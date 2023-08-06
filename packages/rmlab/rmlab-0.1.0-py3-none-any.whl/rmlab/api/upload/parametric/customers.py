"""Interface for uploading pricing models data."""

import os
from typing import List, Optional
from rmlab._api.upload import APIUploadInternal
from rmlab._data.enums import (
    CustomersModelKind,
    ParametricModelKind,
)


class APIUploadCustomersModels(APIUploadInternal):
    """Exposes functions for uploading customers models data to the server."""

    async def upload_customers_request_model(
        self,
        scen_id: int,
        data_fn: str,
    ) -> None:
        """Upload to server a parametric model defined in file, modelling how customers request books.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.json) defining the parametric model
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.CUSTOMERS,
            kind=CustomersModelKind.REQUEST,
            data_fn=data_fn,
        )

    async def upload_customers_choice_model(
        self,
        scen_id: int,
        data_fn: str,
    ) -> None:
        """Upload to server a parametric model defined in file, modelling how customers choose between competing book offers.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.json) defining the parametric model
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.CUSTOMERS,
            kind=CustomersModelKind.CHOICE,
            data_fn=data_fn,
        )

    async def upload_batch_customers_models(
        self,
        scen_id: int,
        *,
        request_models_fns: Optional[List[str]] = None,
        choice_models_fns: Optional[List[str]] = None,
    ):
        if request_models_fns is None:
            request_models_fns = list()
        if choice_models_fns is None:
            request_models_fns = list()

        not_existing_fns = [
            fn for fn in request_models_fns if fn and not os.path.exists(fn)
        ] + [fn for fn in choice_models_fns if fn and not os.path.exists(fn)]

        if len(not_existing_fns) > 0:
            raise FileNotFoundError(not_existing_fns)

        for crm in request_models_fns:

            await self._upload_parametric_model(
                scen_id, ParametricModelKind.CUSTOMERS, CustomersModelKind.REQUEST, crm
            )

        for ccm in choice_models_fns:

            await self._upload_parametric_model(
                scen_id, ParametricModelKind.CUSTOMERS, CustomersModelKind.CHOICE, ccm
            )
