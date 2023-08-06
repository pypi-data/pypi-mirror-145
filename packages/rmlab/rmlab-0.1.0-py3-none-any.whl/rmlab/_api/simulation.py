"""Interface to run simulations and set simulation checkpoint dates."""

import asyncio
from re import A
from typing import Mapping

from tqdm import tqdm
from rmlab._api.fetch import APIFetchInternal


class APISimulationInternal(APIFetchInternal):
    """Exposes functions for simulation."""

    async def _periodic_trigger_progress(
        self, scen_id: int, stop_event: asyncio.Event
    ) -> None:
        """Emits progress bars in the console to track the progress of the simulation.

        Args:
            scen_id (int): Scenario ID in which the simulation is running.
            stop_event (asyncio.Event): Event to notify the stop of the simulation.
        """

        pbars: Mapping[str, tqdm] = dict()

        try:

            (
                dates,
                bounded_count,
                schedules_count,
                flights_count,
            ) = await self._fetch_info(scen_id)

            pbars = {
                "local": tqdm(
                    desc=f"Local progress (SC{scen_id})",
                    unit="day",
                    total=(dates.next - dates.current).days,
                    initial=0,
                ),
                "global": tqdm(
                    desc=f"Global progress (SC{scen_id})",
                    unit="day",
                    total=(dates.last_flight_departure - dates.first_flight_load).days,
                    initial=(dates.current - dates.first_flight_load).days,
                ),
            }

            while not stop_event.is_set():

                await asyncio.sleep(2)

                (
                    dates,
                    bounded_count,
                    schedules_count,
                    flights_count,
                ) = await self._fetch_info(scen_id)

                # TODO: Make these prints compatible with progress bars:
                # print(f"Flights (past/live/pending): {flights_count.past}/{flights_count.live}/{flights_count.pending}              ", end='\r')
                # print(f"Schedules (past/live/pending): {schedules_count.past}/{schedules_count.live}/{schedules_count.pending}              ", end='\r')
                pbars["local"].n = (
                    pbars["local"].total - (dates.next - dates.current).days
                )
                pbars["global"].n = (
                    pbars["global"].total
                    - (dates.last_flight_departure - dates.current).days
                )

                for pb in pbars.values():
                    pb.update()

        except Exception:

            raise

        finally:

            for pb in pbars.values():
                pb.close()
