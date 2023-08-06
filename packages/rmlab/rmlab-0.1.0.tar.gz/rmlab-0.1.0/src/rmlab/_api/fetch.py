from typing import Any, List, Mapping, Optional, Tuple

from rmlab._data.enums import FlightDataKind, ScenarioState
from rmlab._data.types import (
    AirlineLocation,
    BoundedItem,
    UnboundedItem,
    fields_of_dataclass,
)
from rmlab_http_client import Cache

from rmlab._api.base import APIBaseInternal
from rmlab._data.conversions import S2C_DataKind2ConvertFunction
from rmlab.data.scenario import (
    ItemsCount,
    FlightsCount,
    ScenarioDates,
    SchedulesCount,
)
from rmlab.data.items import (
    AirlineLocationItems,
    AllBoundedItems,
    AnyAirlineLocationType,
    AnyBoundedType,
    AnyUnboundedType,
    Flight,
    Schedule,
)
from rmlab.data.flight import FlightData


class APIFetchInternal(APIBaseInternal):
    """Interface to fetch data from server."""

    async def _fetch_info(
        self, scen_id: int
    ) -> Tuple[ScenarioDates, ItemsCount, SchedulesCount, FlightsCount]:
        """Fetch summarized information about a scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            Summary information about a scenario.
        """

        summary = await self._submit_call(
            "api-data-summary-get-single", scen_id=scen_id
        )

        return self._process_summary(scen_id, summary)

    def _process_summary(
        self, scen_id: int, summary: Mapping[str, Any]
    ) -> Tuple[ScenarioDates, ItemsCount, SchedulesCount, FlightsCount]:

        return (
            ScenarioDates(
                id=scen_id,
                upload_time=summary["upload_time"],
                checkpoints=summary["checkpoints"],
                state=ScenarioState.str_to_enum_value(summary["state"]),
                **summary["dates"],
            ),
            ItemsCount(
                id=scen_id,
                **{
                    bi.__name__.lower(): summary["itemsCount"][bi.__name__.lower()]
                    for bi in AllBoundedItems
                },
            ),
            SchedulesCount(
                id=scen_id,
                **summary["itemsCount"][Schedule.__name__.lower()],
            ),
            FlightsCount(
                id=scen_id,
                **summary["itemsCount"][Flight.__name__.lower()],
            ),
        )

    async def _fetch_bounded_items(
        self, scen_id: int, category: AnyBoundedType
    ) -> List[BoundedItem]:
        """Fetch a list of items of bounded category from server.

        Args:
            scen_id (int): Scenario ID
            category (AnyBoundedType): Category of items

        Raises:
            ValueError: If category is not bounded

        Returns:
            List[BoundedItem]: List of bounded items
        """

        if not issubclass(category, BoundedItem):
            raise ValueError(
                f"Category `{category.__name__}` must inherit from `BoundedItem`"
            )

        resp_data = await self._submit_call(
            "api-data-bounded-get-all",
            scen_id=scen_id,
            category=category.__name__.lower(),
        )

        return [category(**itm) for itm in resp_data["items"]]

    async def _fetch_airline_locations_ids(
        self, scen_id: int, airline_id: str, location_type: AnyAirlineLocationType
    ) -> List[str]:
        """Fetch a list of location identifiers associated to an airline from server.
        Used To fetch identifiers of all sectors / citysectors / routes / cityroutes covered by an airline.
        Eg: await api._fetch_airline_locations_ids(scen_id=0, airline_id='MyAirline', location_type=rmlab.data.types.Sector)

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            location_type (AnyAirlineLocationType): Class type, any of `Sector`, `Citysector`, `Route`, `CityRoute`, of `rmlab.data.types` module

        Raises:
            ValueError: If location type is invalid

        Returns:
            List[str]: List of location identifiers
        """

        if location_type not in AirlineLocationItems:
            raise ValueError(
                f"Location type must be one of `{AirlineLocationItems}`, got `{location_type}`"
            )

        return await self._submit_call(
            "api-data-airline-locations-get-ids",
            scen_id=scen_id,
            airline_id=airline_id,
            location_type=location_type.__name__.lower(),
        )

    async def _fetch_airline_locations_items(
        self, scen_id: int, airline_id: str, location_type: AnyAirlineLocationType
    ) -> List[AirlineLocation]:
        """Fetch a list of location items associated to an airline from server.
        Used To fetch items of all sectors / citysectors / routes / cityroutes covered by an airline.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            location_type (AnyAirlineLocationType): Class type, any of `Sector`, `Citysector`, `Route`, `CityRoute`, of `rmlab.data.types` module

        Raises:
            ValueError: If location type is invalid

        Returns:
            List[AirlineLocation]: List of location items
        """

        if location_type not in AirlineLocationItems:
            raise ValueError(
                f"Location type must be one of `{AirlineLocationItems}`, got `{location_type}`"
            )

        items = await self._submit_call(
            "api-data-airline-locations-get-items",
            scen_id=scen_id,
            airline_id=airline_id,
            location_type=location_type.__name__.lower(),
        )

        return [location_type(**item) for item in items]

    async def _fetch_unbounded_ids(
        self,
        scen_id: int,
        category: AnyUnboundedType,
        *,
        citysector_id: Optional[str] = None,
        airline_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[str]:
        """Fetch all identifiers of an unbounded category associated to a citysector, sector (and/or) airline from server.
        At least `citysector_id` and/or `sector_id` must be defined.

        Args:
            scen_id (int): Scenario ID
            category (AnyUnboundedType): Unbounded category (ie: `rmlab.api.data.types.Schedule` or `rmlab.api.data.types.Flight`)
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            airline_id (Optional[str], optional): Target airline ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If category is not unbounded
            ValueError: If none of `citysector_id`, `airline_id`, `sector_id` is defined
            ValueError: If only `airline_id` is defined

        Returns:
            List[str]: List of identifiers of unbounded items.
        """

        if not issubclass(category, UnboundedItem):
            raise ValueError(
                f"Category `{category.__name__}` must inherit from `UnboundedItem`"
            )

        if airline_id is None and citysector_id is None and sector_id is None:
            raise ValueError(
                f"Require definition of `citysector_id`, `airline_id` or `sector_id`"
            )

        if airline_id is not None and (citysector_id is None and sector_id is None):
            raise ValueError(
                f"Required definition of `citysector_id` and/or `sector_id` when airline_id is defined"
            )

        return await self._submit_call(
            "api-data-unbounded-get-ids",
            scen_id=scen_id,
            category=category.__name__.lower(),
            citysector_id=citysector_id,
            airline_id=airline_id,
            sector_id=sector_id,
        )

    async def _fetch_unbounded_items(
        self,
        scen_id: int,
        category: AnyUnboundedType,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[UnboundedItem]:
        """Fetch all items of an unbounded category associated to a citysector or sector from server.
        At least `citysector_id` and/or `sector_id` associated to the items must be defined.

        Args:
            scen_id (int): Scenario ID
            category (AnyUnboundedType): Unbounded category (ie: `rmlab.api.data.types.Schedule` or `rmlab.api.data.types.Flight`)
            ids (List[str]): List of flights schedules or flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If category is not unbounded
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List[UnboundedItem]: List of items of unbounded category.
        """

        if not issubclass(category, UnboundedItem):
            raise ValueError(
                f"Category `{category.__name__}` must inherit from `UnboundedItem`"
            )

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"At least one of `citysector_id`, `sector_id` must be defined"
            )

        fields = fields_of_dataclass(category)

        endpoint_id = "api-data-unbounded-get-fields"
        ep = Cache.get_endpoint(endpoint_id)

        endpoint_limit = ep.arguments.limit_of("ids")
        if endpoint_limit is None:
            endpoint_limit = float("inf")

        if len(ids) > endpoint_limit:

            # Sequentially fetch items in chunks to keep the request/response payloads and server load controlled

            ret_fields: List[UnboundedItem] = list()

            for chunk_start in range(0, len(ids), endpoint_limit):

                chunk_end = chunk_start + endpoint_limit
                if chunk_end > len(ids):
                    chunk_end = -1

                raw_list = await self._submit_call(
                    endpoint_id,
                    scen_id=scen_id,
                    category=category.__name__.lower(),
                    citysector_id=citysector_id,
                    sector_id=sector_id,
                    ids=ids[chunk_start:chunk_end],
                    fields=fields,
                )

                ret_fields += [category(**fields) for fields in raw_list]

            return ret_fields

        else:

            raw_list = await self._submit_call(
                endpoint_id,
                scen_id=scen_id,
                category=category.__name__.lower(),
                citysector_id=citysector_id,
                sector_id=sector_id,
                ids=ids,
                fields=fields,
            )

            return [category(**fields) for fields in raw_list]

    async def _fetch_flights_data(
        self,
        scen_id: int,
        ids: List[str],
        kind: FlightDataKind,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[FlightData]:
        """Fetch flight data arrays of given flights, associated to a citysector or sector, from server.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            kind (FlightDataKind): Kind of flight data to fetch
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List[FlightData]: List of containers holding the flight data arrays.
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"Require definition of either `citysector_id` or `sector_id`"
            )

        endpoint_id = "api-data-flight-get"
        ep = Cache.get_endpoint(endpoint_id)

        endpoint_limit = ep.arguments.limit_of("ids")
        if endpoint_limit is None:
            endpoint_limit = float("inf")

        if len(ids) > endpoint_limit:

            # Sequentially fetch items in chunks to keep the request/response payloads and server load controlled

            ret_data: List[FlightData] = list()

            for chunk_start in range(0, len(ids), endpoint_limit):

                chunk_end = chunk_start + endpoint_limit
                if chunk_end > len(ids):
                    chunk_end = -1

                flights_data = await self._submit_call(
                    endpoint_id,
                    scen_id=scen_id,
                    ids=ids[chunk_start:chunk_end],
                    kind=kind.value,
                    citysector_id=citysector_id,
                    sector_id=sector_id,
                )

                ret_data += [
                    S2C_DataKind2ConvertFunction[kind](flight_id, flight_data)
                    for flight_id, flight_data in zip(
                        ids[chunk_start:chunk_end], flights_data
                    )
                ]

            return ret_data

        else:

            flights_data = await self._submit_call(
                endpoint_id,
                scen_id=scen_id,
                ids=ids,
                kind=kind.value,
                citysector_id=citysector_id,
                sector_id=sector_id,
            )

            return [
                S2C_DataKind2ConvertFunction[kind](flight_id, flight_data)
                for flight_id, flight_data in zip(ids, flights_data)
            ]
