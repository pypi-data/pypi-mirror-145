"""Interface for core items data fetching."""

from typing import List, Optional, Tuple
from rmlab.data.items import (
    Aircraft,
    Airline,
    Airport,
    City,
    CityRoute,
    CitySector,
    Country,
    Flight,
    Route,
    Schedule,
    Sector,
)


from rmlab._api.fetch import APIFetchInternal
from rmlab.data.scenario import (
    ItemsCount,
    FlightsCount,
    ScenarioDates,
    SchedulesCount,
)


class APIFetchCore(APIFetchInternal):
    """Exposes functions for fetching core items data from the server."""

    async def fetch_info(
        self, scen_id: int
    ) -> Tuple[ScenarioDates, ItemsCount, SchedulesCount, FlightsCount]:
        """Fetch summarized information about a scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            A 4-tuple with information about the scenario.
        """

        return await self._fetch_info(scen_id)

    async def fetch_aircrafts(self, scen_id: int) -> List[Aircraft]:
        """Fetch a list of all aircrafts of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of aircrafts
        """

        return await self._fetch_bounded_items(scen_id, Aircraft)

    async def fetch_airlines(self, scen_id: int) -> List[Airline]:
        """Fetch a list of all airlines of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of airlines
        """

        return await self._fetch_bounded_items(scen_id, Airline)

    async def fetch_airports(self, scen_id: int) -> List[Airport]:
        """Fetch a list of all airport of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of airport
        """

        return await self._fetch_bounded_items(scen_id, Airport)

    async def fetch_countries(self, scen_id: int) -> List[Country]:
        """Fetch a list of all countries of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of countries
        """

        return await self._fetch_bounded_items(scen_id, Country)

    async def fetch_cities(self, scen_id: int) -> List[City]:
        """Fetch a list of all cities of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of cities
        """

        return await self._fetch_bounded_items(scen_id, City)

    async def fetch_citysectors(self, scen_id: int) -> List[CitySector]:
        """Fetch a list of all citysectors of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of citysectors
        """

        return await self._fetch_bounded_items(scen_id, CitySector)

    async def fetch_sectors(self, scen_id: int) -> List[Sector]:
        """Fetch a list of all sectors of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of sectors
        """

        return await self._fetch_bounded_items(scen_id, Sector)

    async def fetch_cityroutes(self, scen_id: int) -> List[CityRoute]:
        """Fetch a list of all cityroutes of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of cityroutes
        """

        return await self._fetch_bounded_items(scen_id, CityRoute)

    async def fetch_routes(self, scen_id: int) -> List[Route]:
        """Fetch a list of all routes of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of routes
        """

        return await self._fetch_bounded_items(scen_id, Route)

    async def fetch_airline_sectors(
        self, scen_id: int, airline_id: str
    ) -> List[Sector]:
        """Fetch a list of sectors associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of sectors
        """

        return await self._fetch_airline_locations_items(scen_id, airline_id, Sector)

    async def fetch_airline_citysectors(
        self, scen_id: int, airline_id: str
    ) -> List[CitySector]:
        """Fetch a list of citysectors associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of citysectors
        """

        return await self._fetch_airline_locations_items(
            scen_id, airline_id, CitySector
        )

    async def fetch_airline_routes(self, scen_id: int, airline_id: str) -> List[Route]:
        """Fetch a list of routes associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of routes
        """

        return await self._fetch_airline_locations_items(scen_id, airline_id, Route)

    async def fetch_airline_cityroutes(
        self, scen_id: int, airline_id: str
    ) -> List[CityRoute]:
        """Fetch a list of cityroutes associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of cityroutes
        """

        return await self._fetch_airline_locations_items(scen_id, airline_id, CityRoute)

    async def fetch_airline_sectors_ids(
        self, scen_id: int, airline_id: str
    ) -> List[str]:
        """Fetch a list of sectors ids associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of sectors
        """

        return await self._fetch_airline_locations_ids(scen_id, airline_id, Sector)

    async def fetch_airline_citysectors_ids(
        self, scen_id: int, airline_id: str
    ) -> List[str]:
        """Fetch a list of citysectors ids associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of citysectors
        """

        return await self._fetch_airline_locations_ids(scen_id, airline_id, CitySector)

    async def fetch_airline_routes_ids(
        self, scen_id: int, airline_id: str
    ) -> List[str]:
        """Fetch a list of routes ids associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of routes
        """

        return await self._fetch_airline_locations_ids(scen_id, airline_id, Route)

    async def fetch_airline_cityroutes_ids(
        self, scen_id: int, airline_id: str
    ) -> List[str]:
        """Fetch a list of cityroutes associated to an airline from server.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID

        Returns:
            List of cityroutes
        """

        return await self._fetch_airline_locations_ids(scen_id, airline_id, CityRoute)

    async def fetch_schedules_ids(
        self,
        scen_id: int,
        *,
        citysector_id: Optional[str] = None,
        airline_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[str]:
        """Fetch all flights schedules identifiers associated to a citysector or sector from server.
        At least `citysector_id` and/or `sector_id` associated to the items must be defined.

        Args:
            scen_id (int): Scenario ID
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            airline_id (Optional[str], optional): Target airline ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If none of `citysector_id`, `airline_id`, `sector_id` is defined
            ValueError: If only `airline_id` is defined

        Returns:
            List of identifiers of unbounded items
        """

        return await self._fetch_unbounded_ids(
            scen_id,
            Schedule,
            citysector_id=citysector_id,
            airline_id=airline_id,
            sector_id=sector_id,
        )

    async def fetch_schedules(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[Schedule]:
        """Fetch all flights schedules associated to a citysector or sector from server.
        At least `citysector_id` and/or `sector_id` associated to the items must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of schedules IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of flights schedules.
        """

        return await self._fetch_unbounded_items(
            scen_id, Schedule, ids, citysector_id=citysector_id, sector_id=sector_id
        )

    async def fetch_flights_ids(
        self,
        scen_id: int,
        *,
        citysector_id: Optional[str] = None,
        airline_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[str]:
        """Fetch all flights identifiers associated to a citysector or sector from server.
        At least `citysector_id` and/or `sector_id` associated to the items must be defined.

        Args:
            scen_id (int): Scenario ID
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            airline_id (Optional[str], optional): Target airline ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If none of `citysector_id`, `airline_id`, `sector_id` is defined
            ValueError: If only `airline_id` is defined

        Returns:
            List of identifiers of unbounded items
        """

        return await self._fetch_unbounded_ids(
            scen_id,
            Flight,
            citysector_id=citysector_id,
            airline_id=airline_id,
            sector_id=sector_id,
        )

    async def fetch_flights(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[Flight]:
        """Fetch all flights associated to a citysector or sector from server.
        At least `citysector_id` and/or `sector_id` associated to the items must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None
            sector_id (Optional[str], optional): Target sector ID. Defaults to None

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of flights
        """

        return await self._fetch_unbounded_items(
            scen_id, Flight, ids, citysector_id=citysector_id, sector_id=sector_id
        )
