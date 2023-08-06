"""Interface for uploading customers models data."""

import os
from typing import List, Optional
from rmlab._api.upload import APIUploadInternal
from rmlab._data.enums import (
    ParametricModelKind,
    PricingModelKind,
)


class APIUploadPricingModels(APIUploadInternal):
    """Exposes functions for uploading pricing models data to the server."""

    async def upload_pricing_range_model(
        self,
        scen_id: int,
        data_fn: str,
    ) -> None:
        """Upload to server a parametric model defined in file, specifying a pricing range to be applied by flights.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.json) defining the parametric model
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.RANGE,
            data_fn=data_fn,
        )

    async def upload_pricing_behavior_model(
        self,
        scen_id: int,
        data_fn: str,
    ) -> None:
        """Upload to server a parametric model defined in file, specifying the pricing behavior/strategy
        under which flights assign prices to seats.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.json) defining the parametric model
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.BEHAVIOR,
            data_fn=data_fn,
        )

    async def upload_pricing_optimizer_model(
        self,
        scen_id: int,
        data_fn: str,
    ) -> None:
        """Upload to server a parametric model defined in file, specifying the pricing optimization methods
        under which flights operate, to adapt the prices given current and past demand.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.json) defining the parametric model
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.OPTIMIZER,
            data_fn=data_fn,
        )

    async def upload_batch_pricing_models(
        self,
        scen_id: int,
        *,
        range_models_fns: Optional[List[str]] = None,
        behavior_models_fns: Optional[List[str]] = None,
        optimizer_models_fns: Optional[List[str]] = None,
    ):
        if range_models_fns is None:
            range_models_fns = list()
        if behavior_models_fns is None:
            behavior_models_fns = list()
        if optimizer_models_fns is None:
            optimizer_models_fns = list()

        not_existing_fns = (
            [fn for fn in range_models_fns if fn and not os.path.exists(fn)]
            + [fn for fn in behavior_models_fns if fn and not os.path.exists(fn)]
            + [fn for fn in optimizer_models_fns if fn and not os.path.exists(fn)]
        )

        if len(not_existing_fns) > 0:
            raise FileNotFoundError(not_existing_fns)

        for prm in range_models_fns:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.RANGE, prm
            )

        for pbm in behavior_models_fns:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.BEHAVIOR, pbm
            )

        for pom in optimizer_models_fns:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.OPTIMIZER, pom
            )
