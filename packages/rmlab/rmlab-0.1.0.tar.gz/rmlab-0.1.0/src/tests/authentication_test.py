import os, pytest
from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from rmlab_http_client import Cache
from rmlab._api.base import (
    APIBaseInternal,
    BaseURL,
    _ExpectedCredentialsKeys,
    _ExpectedEndpointsIds,
)
from rmlab_errors import AuthenticationError
from rmlab._version import __version__

import os


@dataclass
class TestLoginData:
    workgroup: str
    username: str
    password: str


@dataclass
class TestBaseURLs:
    api: str
    auth: str


@pytest.fixture
def base_urls():

    return TestBaseURLs(
        api=os.environ.get("RMLAB_URL_API") or BaseURL,
        auth=os.environ.get("RMLAB_URL_AUTH") or BaseURL,
    )


@pytest.fixture
def login_data():

    return TestLoginData(
        workgroup=os.environ["RMLAB_WORKGROUP"],
        username=os.environ["RMLAB_USERNAME"],
        password=os.environ["RMLAB_PASSWORD"],
    )


def test_web_is_up(base_urls):

    headers = {"User-Agent": "Mozilla/5.0"}

    if BaseURL in base_urls.api:
        # Expect correct html response
        assert urlopen(Request(base_urls.api, headers=headers)).getcode() == 200
        assert urlopen(Request(base_urls.auth, headers=headers)).getcode() == 200
    else:
        # Testing/Dev API only. Expect not found (404) response since '/' resource is not defined
        with pytest.raises(HTTPError):
            urlopen(Request(base_urls.api, headers=headers))
            urlopen(Request(base_urls.auth, headers=headers))


async def test_session_implicit_args():

    Cache._credentials = None
    Cache._endpoints = None

    async with APIBaseInternal():
        pass

    for ep_id in _ExpectedEndpointsIds:
        assert ep_id in Cache._endpoints

    for cred_id in _ExpectedCredentialsKeys:
        assert cred_id in Cache._credentials


async def test_session_explicit_args(login_data):

    Cache._credentials = None
    Cache._endpoints = None

    async with APIBaseInternal(**login_data.__dict__):
        pass

    for ep_id in _ExpectedEndpointsIds:
        assert ep_id in Cache._endpoints

    for cred_id in _ExpectedCredentialsKeys:
        assert cred_id in Cache._credentials


async def test_session_fail():

    Cache._credentials = None
    Cache._endpoints = None

    with pytest.raises(AuthenticationError):
        async with APIBaseInternal(
            workgroup="wrong-workgroup", username="wrong-user", password="wrong-pwd"
        ):
            pass
