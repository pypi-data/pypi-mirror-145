"""Interface for fetching flight data."""

from typing import List, Optional
from rmlab._data.enums import FlightDataKind
from rmlab._api.fetch import APIFetchInternal

from rmlab.data.flight import (
    FlightDataBooks,
    FlightDataEvents,
    FlightDataPricePerSeatSettings,
    FlightDataThresholdSettings,
)


class APIFetchFlightData(APIFetchInternal):
    """Exposes functions for fetching flight data from the server."""

    async def fetch_flights_data_historic(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[FlightDataBooks]:
        """Fetch flight data of historic books of given flights, associated to a citysector or sector, from server.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of historic books data containers of each flight.
        """

        return await self._fetch_flights_data(
            scen_id,
            ids,
            FlightDataKind.ACTUAL_BOOKS,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def fetch_flights_data_pricing_thresholds(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[FlightDataThresholdSettings]:
        """Fetch flight data of pricing thresholds of given flights, associated to a citysector or sector, from server.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of pricing thresholds data containers of each flight.
        """

        return await self._fetch_flights_data(
            scen_id,
            ids,
            FlightDataKind.THRESHOLDS_SETTINGS,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def fetch_flights_data_pricing_per_seat(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[FlightDataPricePerSeatSettings]:
        """Fetch flight data of pricing per seat of given flights, associated to a citysector or sector, from server.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of pricing per seat data containers of each flight.
        """

        return await self._fetch_flights_data(
            scen_id,
            ids,
            FlightDataKind.PRICE_PER_SEAT_SETTINGS,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def fetch_flights_data_events(
        self,
        scen_id: int,
        ids: List[str],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> List[FlightDataEvents]:
        """Fetch flight data of events of given flights, associated to a citysector or sector, from server.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            ids (List[str]): List of flights IDs
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined

        Returns:
            List of events data containers of each flight.
        """

        return await self._fetch_flights_data(
            scen_id,
            ids,
            FlightDataKind.EVENTS,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )
