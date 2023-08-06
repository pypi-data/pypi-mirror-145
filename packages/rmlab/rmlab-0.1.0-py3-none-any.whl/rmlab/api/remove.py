"""Interface for remote data removal

This script provides a APIRemove context manager exposing functions 
for removing data from the server.
"""

from rmlab._api.remove import APIRemoveInternal
from rmlab._data.enums import DataRemoveKind


class APIRemove(APIRemoveInternal):
    """Interface to upload data to server"""

    async def remove_data_full(self, scen_id: int) -> None:
        """Remove all the data of a scenario.

        Args:
            scen_id (int): Scenario ID
        """

        await self._remove_data(scen_id, DataRemoveKind.COMPLETE)

    async def remove_data_historic(self, scen_id: int) -> None:
        """Remove all the historic flight data of a scenario.

        Args:
            scen_id (int): Scenario ID
        """

        await self._remove_data(scen_id, DataRemoveKind.HISTORIC)
