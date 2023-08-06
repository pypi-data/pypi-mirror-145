"""Interface for fetching data related to parametric models and filters."""

from typing import List
from rmlab.data.items import PModel
from rmlab.data.parametric.filter import PFilter
from rmlab._api.fetch import APIFetchInternal


class APIFetchParametric(APIFetchInternal):
    """Exposes functions for fetching flight data from the server."""

    async def fetch_parametric_filters(self, scen_id: int) -> List[PFilter]:
        """Fetch a list of all parametric filters of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of parametric filters
        """

        return await self._fetch_bounded_items(scen_id, PFilter)

    async def fetch_parametric_models(self, scen_id: int) -> List[PModel]:
        """Fetch a list of all parametric models of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of parametric models
        """

        return await self._fetch_bounded_items(scen_id, PModel)
