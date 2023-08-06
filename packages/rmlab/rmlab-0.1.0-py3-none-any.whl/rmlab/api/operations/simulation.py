"""Interface for running simulations."""

import asyncio
from datetime import datetime
from typing import List, Optional, Tuple

from rmlab._data.types import DateFormat
from rmlab._api.simulation import APISimulationInternal
from rmlab.data.scenario import (
    ItemsCount,
    FlightsCount,
    ScenarioDates,
    SchedulesCount,
)


class APISimulation(APISimulationInternal):
    """Exposes functions for running simulations on server and adding simulation checkpoints."""

    async def upload_checkpoints(
        self, scen_id: int, checkpoints: List[datetime]
    ) -> None:
        """Upload date checkpoints at which simulation is paused.

        Args:
            scen_id (int): Scenario ID in which the simulation is running
            checkpoints (List[datetime]): List of checkpoints
        """

        await self._submit_call(
            "api-operation-simulation-checkpoint",
            scen_id=scen_id,
            checkpoints=[datetime.strftime(chp, DateFormat) for chp in checkpoints],
        )

    async def trigger_simulation(
        self, scen_id: int, next: Optional[datetime] = None
    ) -> Tuple[ScenarioDates, ItemsCount, SchedulesCount, FlightsCount]:
        """Trigger a simulation run on a given scenario.

        Args:
            scen_id (int): Scenario ID
            next (Optional[datetime], optional): Checkpoint at which the simulation is stopped. Defaults to None.

        Raises:
            ValueError: If the type of `next` is invalid
            RuntimeError: If simulation failed for any reason

        Returns:
            Summarized information of the scenario after the simulation finishes
        """

        if next is not None:
            if not isinstance(next, datetime):
                raise ValueError(
                    f"Expected `datetime` type in `next` {next}, got `{type(next)}`"
                )

            await self._submit_call(
                "api-operation-simulation-checkpoint",
                scen_id=scen_id,
                checkpoints=[datetime.strftime(next, DateFormat)],
            )

        trigger_task = asyncio.create_task(
            self._submit_call(
                "api-operation-simulation-trigger", scen_id=scen_id, operation="auto"
            )
        )

        stop_event = asyncio.Event()

        progress_task = asyncio.create_task(
            self._periodic_trigger_progress(scen_id, stop_event)
        )

        await asyncio.wait(
            [trigger_task, progress_task],
            timeout=None,
            return_when=asyncio.FIRST_COMPLETED,
        )

        if not stop_event.is_set() and not progress_task.done():
            stop_event.set()
            await progress_task

        exc = progress_task.exception()
        if exc is not None:
            raise RuntimeError(f"Error {type(exc)} while tracking progress: {exc}")

        summary = trigger_task.result()

        return self._process_summary(scen_id, summary)
