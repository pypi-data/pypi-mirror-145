"""Script exposing the core underlying API functions, handling authentication and API calls."""

import os, logging
from types import MethodType
from typing import Any, Iterable, List, Mapping, Optional

from rmlab_errors import raise_from_list

from rmlab_http_client import (
    AsyncClient,
    AuthType,
    Endpoint,
    PayloadArguments,
    ResponseType,
    SyncClient,
    MethodType,
    CommunicationType,
    PayloadType,
    DataRequestContext,
    DataRequestContextMultipart,
    Cache,
)

# Endpoint to discover dynamic protected auth endpoints
DiscoverAuthEndpoint = Endpoint(
    resource=["auth", "discover"],
    method=MethodType.GET,
    payload=PayloadType.NONE,
    arguments=PayloadArguments(),
    auth=AuthType.PUBLIC,
    response=ResponseType.JSON,
    id="auth-discover",
)

from rmlab._version import __version__

_Logger = logging.getLogger(__name__)

BaseURL = "https://rmlab.net"

_ExpectedCredentialsKeys = [
    "access_token",
    "refresh_token",
    "services",
    "scenarios",
    "username",
    "workgroup",
]

_ExpectedEndpointsIds = [
    "auth-log-in",
    "auth-log-in-poll-status",
    "auth-log-in-result",
    "auth-log-out",
    "auth-token-refresh",
    "api-discover-user",
    "api-data-bounded-get-meta",
    "api-data-bounded-get-all",
    "api-data-bounded-get-single",
    "api-data-bounded-post",
    "api-data-flight-get",
    "api-data-flight-post",
    "api-data-flight-thresholds-post",
    "api-data-pmodel-post",
    "api-data-unbounded-get-fields",
    "api-data-unbounded-get-ids",
    "api-data-unbounded-post",
    "api-data-airline-locations-get-ids",
    "api-data-airline-locations-get-items",
    "api-data-remove-full",
    "api-data-remove-restart",
    "api-data-summary-get-all",
    "api-data-summary-get-single",
    "api-operation-simulation-checkpoint",
    "api-operation-simulation-pause",
    "api-operation-simulation-trigger",
    "api-operation-optimization-trigger",
    "api-operation-optimization-schedule",
    "api-monitor-activity-user",
    "api-monitor-async-status",
    "api-monitor-async-result",
]


def _check_valid_credentials(creds: Mapping[str, Any]):

    if not all([k in creds for k in _ExpectedCredentialsKeys]):
        raise ValueError(f"Some required keys not found in received credentials")


def _check_valid_endpoints(endpoints_ids: Iterable[str]):

    errs = list()
    for ep_id in endpoints_ids:
        if ep_id not in _ExpectedEndpointsIds:
            errs.append(RuntimeError(f"Unrecognized endpoint `{ep_id}`"))

    raise_from_list(errs)


class APIBaseInternal:
    """Asynchronous context manager providing internal initialization, login and API server calls to derived classes."""

    def __init__(
        self,
        workgroup: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initializes APIBaseInternal instance.

        Args:
            workgroup: (str, optional): Workgroup name. Defaults to None.
                If none, expects `RMLAB_WORKGROUP` environment variable definition.
            user (str, optional): User name. Defaults to None.
                If none, expects `RMLAB_USERNAME` environment variable definition.
            password (str, optional): Password. Defaults to None.
                If none, expects `RMLAB_PASSWORD` environment variable definition..

        Raises:
            AuthenticationError: If user or password are not defined.
        """

        if any([arg is None for arg in [workgroup, username, password]]):

            try:
                workgroup = os.environ["RMLAB_WORKGROUP"]
                username = os.environ["RMLAB_USERNAME"]
                password = os.environ["RMLAB_PASSWORD"]

            except KeyError:

                raise ValueError(
                    f"`RMLAB_WORKGROUP` / `RMLAB_USERNAME` / `RMLAB_PASSWORD` are undefined"
                )

        Cache.set_credential(
            "basic_auth", ":".join([workgroup, username, password, __version__])
        )

        self._url_api = os.environ.get("RMLAB_URL_API") or BaseURL
        self._url_auth = os.environ.get("RMLAB_URL_AUTH") or BaseURL

    @classmethod
    @property
    def scenarios(cls) -> List[int]:
        scenarios = Cache.get_credential("scenarios")
        if scenarios:
            return [sc_id for sc_id in scenarios.keys()]
        else:
            raise ValueError(f"Scenarios not initialized")

    async def __aenter__(self):
        """Context manager asynchronous enter.
        If credentials are not defined:
        1. Fetch and cache dynamic authentication endpoints
        2. Uses those endpoints to log-in, and cache credentials
        3. Fetch and cache dynamic api endpoints

        Returns:
            APIBaseInternal: This instance.
        """

        if Cache.get_credential("access_token") is None:

            async with SyncClient(
                DiscoverAuthEndpoint, address=self._url_auth
            ) as discover_auth_client:

                auth_endpoints = await discover_auth_client.submit_request()
                _check_valid_endpoints(auth_endpoints.keys())
                Cache.add_endpoints(**auth_endpoints)

            async with AsyncClient(
                address=self._url_auth,
                async_endpoint=Cache.get_endpoint("auth-log-in"),
                poll_endpoint=Cache.get_endpoint("auth-log-in-poll-status"),
                result_endpoint=Cache.get_endpoint("auth-log-in-result"),
            ) as login_client:

                _Logger.debug("Logging-in...")

                creds = await login_client.submit_request()
                _check_valid_credentials(creds)
                for ck, cv in creds.items():
                    Cache.set_credential(ck, cv)

                endpoints: Mapping[str, dict] = creds.pop("endpoints")
                _check_valid_endpoints(endpoints.keys())
                Cache.add_endpoints(**endpoints)

            async with SyncClient(
                Cache.get_endpoint("api-discover-user"),
                address=self._url_api,
                refresh_address=self._url_auth,
                refresh_endpoint=Cache.get_endpoint("auth-token-refresh"),
            ) as discover_api_client:

                api_endpoints = await discover_api_client.submit_request()
                _check_valid_endpoints(api_endpoints.keys())
                Cache.add_endpoints(**api_endpoints)

        return self

    async def __aexit__(self, exc_ty, exc_val, exc_tb):
        """Context manager asynchronous exit.
        Submits log-out to server, but does not re-raise any eventual error"""

        try:

            async with SyncClient(
                Cache.get_endpoint("auth-log-out"), address=self._url_auth
            ) as logout_client:

                await logout_client.submit_request()

        except Exception:
            # Do not propagate exceptions due to log-out
            pass

    async def _submit_call(self, endpoint_id: str, **kwargs) -> Any:
        """Submit API call to a specific server endpoint.

        Args:
            endpoint_id (str): Endpoint identifier

        Raises:
            RuntimeError: If endpoint does not exist
            ValueError: If arguments do not match endpoint requirements

        Returns:
            Any: API response
        """

        ep = Cache.get_endpoint(endpoint_id)

        context_type = (
            DataRequestContextMultipart
            if ep.payload == PayloadType.MULTIPART
            else DataRequestContext
        )

        with context_type(ep, **kwargs) as rdc:

            if ep.communication == CommunicationType.SYNC:

                async with SyncClient(
                    ep,
                    address=self._url_api,
                    refresh_address=self._url_auth,
                    refresh_endpoint=Cache.get_endpoint("auth-token-refresh"),
                ) as sync_client:

                    return await sync_client.submit_request(rdc.data)

            else:

                assert ep.communication == CommunicationType.ASYNC

                async with AsyncClient(
                    address=self._url_api,
                    async_endpoint=ep,
                    poll_endpoint=Cache.get_endpoint(ep.async_poll_endpoint_id),
                    result_endpoint=Cache.get_endpoint(ep.async_result_endpoint_id),
                    refresh_address=self._url_auth,
                    refresh_endpoint=Cache.get_endpoint("auth-token-refresh"),
                ) as async_client:

                    return await async_client.submit_request(rdc.data)
