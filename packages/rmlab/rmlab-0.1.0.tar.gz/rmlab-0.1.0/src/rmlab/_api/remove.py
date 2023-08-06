from rmlab._api.base import APIBaseInternal
from rmlab._data.enums import (
    DataRemoveKind,
)


class APIRemoveInternal(APIBaseInternal):
    """Interface to remove data from server."""

    async def _remove_data(self, scen_id: int, kind: DataRemoveKind) -> None:
        """Remove some or all the data of a scenario.

        Args:
            scen_id (int): Scenario ID.
            kind (DataRemoveKind): Type of removal.
        """

        if kind.value == "full":

            await self._submit_call("api-data-remove-full", scen_id=scen_id)

        elif kind.value == "restart":

            await self._submit_call("api-data-remove-restart", scen_id=scen_id)

        else:

            raise ValueError(f"Unknown kind `{kind}`")
