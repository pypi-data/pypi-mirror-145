import os, pathlib
from rmlab.api.fetch.core import APIFetchCore

from rmlab.api.remove import APIRemove
from rmlab.api.operations.simulation import APISimulation
from rmlab.api.upload.core import APIUploadCore
from rmlab.api.upload.parametric.customers import APIUploadCustomersModels
from rmlab.api.upload.parametric.filters import APIUploadParametric
from rmlab.api.upload.parametric.pricing import APIUploadPricingModels
from rmlab.api.fetch.flight_data import APIFetchFlightData

_DataSamplesPath = (
    str(pathlib.Path(os.path.realpath(__file__)).parent.parent) + "/data_samples/"
)


class APISimulationUpload(
    APISimulation,
    APIFetchCore,
    APIFetchFlightData,
    APIUploadCore,
    APIUploadParametric,
    APIUploadCustomersModels,
    APIUploadPricingModels,
    APIRemove,
):
    pass


async def test_analysis():

    async with APISimulationUpload() as api:

        scen_id = api.scenarios[0]

        await api.remove_data_full(scen_id=scen_id)

        # Upload customers models to server
        await api.upload_batch_customers_models(
            scen_id,
            request_models_fns=[
                _DataSamplesPath + "/basic/customers_request.poisson_bl1.json"
            ],
            choice_models_fns=[
                _DataSamplesPath + "/basic/customers_choice.mnl_bl1.json"
            ],
        )

        # Upload pricing models to server
        await api.upload_batch_pricing_models(
            scen_id,
            range_models_fns=[_DataSamplesPath + "/basic/pricing_range.sample.json"],
            behavior_models_fns=[
                _DataSamplesPath + "/basic/pricing_behavior.sample.json"
            ],
            optimizer_models_fns=[
                _DataSamplesPath + "/basic/pricing_optimizer.sample.json"
            ],
        )

        await api.upload_parametric_filters(
            scen_id, data_fn=_DataSamplesPath + "/basic/table.pfilter.json"
        )

        # Upload core items to server
        await api.upload_batch_core(
            scen_id,
            aircraft_items_fn=_DataSamplesPath + "/basic/table.aircraft.csv",
            airline_items_fn=_DataSamplesPath + "/basic/table.airline.csv",
            airport_items_fn=_DataSamplesPath + "/basic/table.airport.csv",
            city_items_fn=_DataSamplesPath + "/basic/table.city.csv",
            country_items_fn=_DataSamplesPath + "/basic/table.country.csv",
            schedule_items_fn=_DataSamplesPath + "/basic/table.schedule.csv",
        )

        await api.trigger_simulation(scen_id)

        csc_items = await api.fetch_citysectors(scen_id)
        assert len(csc_items) > 0

        for csc in csc_items:

            flt_ids = await api.fetch_flights_ids(scen_id, citysector_id=csc.id)
            assert len(flt_ids) > 0

            actual_books = await api.fetch_flights_data_historic(
                scen_id, flt_ids, citysector_id=csc.id
            )
            assert all([not flt_data.is_empty() for flt_data in actual_books])

            threshold_setts = await api.fetch_flights_data_pricing_thresholds(
                scen_id, flt_ids, citysector_id=csc.id
            )
            assert all([not flt_data.is_empty() for flt_data in threshold_setts])

            pps_setts = await api.fetch_flights_data_pricing_per_seat(
                scen_id, flt_ids, citysector_id=csc.id
            )
            assert all([not flt_data.is_empty() for flt_data in pps_setts])

            events = await api.fetch_flights_data_events(
                scen_id, flt_ids, citysector_id=csc.id
            )
            assert all([not flt_data.is_empty() for flt_data in events])
