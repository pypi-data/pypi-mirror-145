from rmlab.api.remove import APIRemove
from rmlab.api.operations.simulation import APISimulation
from rmlab.api.operations.optimization import APIOptimization
from rmlab.api.upload.core import APIUploadCore
from rmlab.api.upload.parametric.filters import APIUploadParametric
from rmlab.api.upload.parametric.customers import APIUploadCustomersModels
from rmlab.api.upload.parametric.pricing import APIUploadPricingModels
from rmlab.api.upload.flight_data import APIUploadFlightData
from rmlab.api.fetch.core import APIFetchCore
from rmlab.api.fetch.flight_data import APIFetchFlightData


class API(
    APISimulation,
    APIOptimization,
    APIUploadCore,
    APIUploadParametric,
    APIUploadCustomersModels,
    APIUploadPricingModels,
    APIUploadFlightData,
    APIRemove,
    APIFetchCore,
    APIFetchFlightData,
):
    """Complete mixin interface to run simulations, upload local data and fetch/remove remote data"""

    pass
