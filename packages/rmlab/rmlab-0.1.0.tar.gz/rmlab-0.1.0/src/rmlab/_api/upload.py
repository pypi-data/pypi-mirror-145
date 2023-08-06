import os, logging
from typing import Optional, Union

from rmlab_http_client.types import FileExtensionType

from rmlab._api.base import APIBaseInternal
from rmlab._data.conversions import (
    C2S_FlightDataName2ConvertFunction,
    UploadableDataClassName2DataKind,
    UploadableFlightDataType,
)
from rmlab._data.enums import (
    CustomersModelKind,
    ParametricModelKind,
    PricingModelKind,
)
from rmlab._data.types import (
    BoundedItem,
    UnboundedItem,
)
from rmlab.data.parametric.customers_choice import make_customers_choice_model_from_json
from rmlab.data.parametric.customers_request import (
    make_customers_request_model_from_json,
)
from rmlab.data.parametric.pricing_behavior import make_pricing_behavior_from_json
from rmlab.data.parametric.pricing_optimizer import make_pricing_optimizer_from_json
from rmlab.data.parametric.pricing_range import make_pricing_range_from_json


_Logger = logging.getLogger(__name__)


class APIUploadInternal(APIBaseInternal):
    """Interface to upload data to server"""

    async def _upload_bounded_items(
        self, scen_id: int, category: BoundedItem, data_fn: str
    ) -> None:
        """Upload a set of bounded items defined in a file.

        Args:
            scen_id (int): Scenario ID
            category (BoundedItem): Category
            data_fn (str): Filename (.csv or .json) defining the items

        Raises:
            ValueError: If category is not bounded
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        if not issubclass(category, BoundedItem):
            raise ValueError(
                f"Category `{category.__name__}` must inherit from `BoundedItem`"
            )

        if not os.path.exists(data_fn):
            raise FileNotFoundError(data_fn)

        _, ext = os.path.splitext(data_fn)
        ext: str = FileExtensionType.str_to_enum_value(ext.replace(".", "")).value

        _Logger.debug(f"Uploading `{category.__name__}` items")

        await self._submit_call(
            "api-data-bounded-post",
            scen_id=scen_id,
            category=category.__name__.lower(),
            file=data_fn,
            extension=ext,
        )

        _Logger.debug(f"File `{data_fn}` of category `{category.__name__}` uploaded")

    async def _upload_unbounded_items(
        self,
        scen_id: int,
        category: UnboundedItem,
        data_fn: str,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> None:
        """Upload a set of unbounded items defined in a file.
        Used to upload a set of flight schedules or a set of flights to server.

        Arguments `citysector_id` and `sector_id` are always optional. If any of them provided, concurrent uploads of flights
            files belonging to different citysectors/sectors are allowed.

        Args:
            scen_id (int): Scenario ID
            category (UnboundedItem): Category
            data_fn (str): Filename (.csv or .json) defining the items
            citysector_id (Optional[str], optional): Citysector ID to which items in file are associated. Defaults to None.
            sector_id (Optional[str], optional): Sector ID to which items in file are associated. Defaults to None.

        Raises:
            ValueError: If category is not unbounded
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        if not issubclass(category, UnboundedItem):
            raise ValueError(
                f"Category `{category.__name__}` must inherit from `UnboundedItem`"
            )

        _, ext = os.path.splitext(data_fn)
        ext: str = FileExtensionType.str_to_enum_value(ext.replace(".", "")).value

        _Logger.debug(f"Uploading `{category.__name__}` items")

        await self._submit_call(
            "api-data-unbounded-post",
            scen_id=scen_id,
            category=category.__name__.lower(),
            citysector_id=citysector_id,
            sector_id=sector_id,
            file=data_fn,
            extension=ext,
        )

        _Logger.debug(f"File `{data_fn}` of category `{category.__name__}` uploaded")

    async def _upload_flight_data(
        self,
        scen_id: int,
        flight_data: UploadableFlightDataType,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> None:
        """Upload flight data to server. Data types can be `FlightDataBooks`, `FlightDataThresholdSettings` or `FlightDataPricePerSeatSettings`.
        Any previous existing data is overwritten.
        At least `citysector_id` and/or `sector_id` associated to the flight must be defined.

        Args:
            scen_id (int): Scenario ID
            flight_data (UploadableFlightDataType): Flight data to upload.
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
            ValueError: If flight data has incorrect type.
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"Require definition of either `citysector_id` or `sector_id`"
            )

        flight_data_class_name = type(flight_data).__name__

        if flight_data_class_name not in UploadableDataClassName2DataKind:
            raise ValueError(
                f"Flight data of type `{type(flight_data)}` cannot be uploaded"
            )

        flight_id, data = C2S_FlightDataName2ConvertFunction[flight_data_class_name](
            flight_data
        )

        kind = UploadableDataClassName2DataKind[flight_data_class_name]

        await self._submit_call(
            "api-data-flight-post",
            scen_id=scen_id,
            flight_id=flight_id,
            kind=kind,
            citysector_id=citysector_id,
            sector_id=sector_id,
            data=data,
        )

    async def _upload_parametric_model(
        self,
        scen_id: int,
        parametric_kind: ParametricModelKind,
        kind: Union[CustomersModelKind, PricingModelKind],
        data_fn: str,
    ) -> None:
        """Upload a parametric model (a `customers` or a `pricing` model) defined in a file to server.

        Args:
            scen_id (int): Scenario ID
            parametric_kind (ParametricModelKind): Parametric kind value (a `customers` or `pricing` parametric model)
            kind (Union[CustomersModelKind, PricingModelKind]): A subkind of parametric model.
            Given parametric_kind=`CUSTOMERS`, any of `REQUEST` or `CHOICE`
            Given parametric_kind=`PRICING`, any of `RANGE`, `BEHAVIOR`, `OPTIMIZER`
            data_fn (str): Filename (.json) defining the parametric model.
        """

        # Make equivalent parametric models types to ensure correctness before uploading to server
        if parametric_kind == ParametricModelKind.CUSTOMERS:
            if kind == CustomersModelKind.REQUEST:
                make_customers_request_model_from_json(data_fn)
            elif kind == CustomersModelKind.CHOICE:
                make_customers_choice_model_from_json(data_fn)
            else:
                raise ValueError(f"Unexpected value of `{kind}`")
        elif parametric_kind == ParametricModelKind.PRICING:
            if kind == PricingModelKind.RANGE:
                make_pricing_range_from_json(data_fn)
            elif kind == PricingModelKind.BEHAVIOR:
                make_pricing_behavior_from_json(data_fn)
            elif kind == PricingModelKind.OPTIMIZER:
                make_pricing_optimizer_from_json(data_fn)
            else:
                raise ValueError(f"Unexpected value of `{kind}`")
        else:
            raise ValueError(f"Unexpected value of `{parametric_kind}`")

        _, ext = os.path.splitext(data_fn)
        ext: str = FileExtensionType.str_to_enum_value(ext.replace(".", "")).value

        _Logger.debug(f"Uploading `{parametric_kind.value}` `{kind.value}` model")

        pmodel_id = os.path.basename(data_fn)

        await self._submit_call(
            "api-data-pmodel-post",
            scen_id=str(scen_id),
            kind=parametric_kind.value + "_" + kind.value,
            pmodel_id=pmodel_id,
            file=data_fn,
            extension=ext,
        )

        _Logger.debug(f"File `{data_fn}` uploaded as pmodel with id `{pmodel_id}`")
