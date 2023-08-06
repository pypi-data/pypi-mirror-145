"""Interface to trigger optimization passes."""

from datetime import datetime
from typing import Optional
from rmlab._api.base import APIBaseInternal
from rmlab._data.types import DateTimeMinFormat


class APIOptimization(APIBaseInternal):
    """Exposes functions to run and schedule optimization runs on a set of flights."""

    async def trigger_optimization_pass(
        self,
        scen_id: int,
        airline_id: str,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ):
        """Triggers an optimization pass on all flights of an airline belonging to a citysector or sector.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            citysector_id (Optional[str], optional): Citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"At least one of `citysector_id`, `sector_id` must be defined"
            )

        await self._submit_call(
            "api-operation-optimize-trigger",
            scen_id=scen_id,
            airline_id=airline_id,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def schedule_optimization_pass(
        self,
        scen_id: int,
        airline_id: str,
        date_time: datetime,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ):
        """Schedules an optimization pass on all flights of an airline belonging to a citysector or sector to be run at specific date and time.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            date_time (datetime): Date and time at which the optimization pass is triggered.
            citysector_id (Optional[str], optional): Citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"At least one of `citysector_id`, `sector_id` must be defined"
            )

        await self._submit_call(
            "api-operation-optimize-schedule",
            scen_id=scen_id,
            date_time=datetime.strftime(date_time, DateTimeMinFormat),
            airline_id=airline_id,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )
