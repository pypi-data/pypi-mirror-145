from rmlab._api.upload import APIUploadInternal
from rmlab.data.parametric.filter import PFilter


class APIUploadParametric(APIUploadInternal):
    """Exposes functions for uploading parametric filters to the server."""

    async def upload_parametric_filters(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of parametric filters defined in a file.

        ```json
        {"json": "example"}
        ```

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.csv or .json) defining the parametric filters

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=PFilter, data_fn=data_fn
        )
