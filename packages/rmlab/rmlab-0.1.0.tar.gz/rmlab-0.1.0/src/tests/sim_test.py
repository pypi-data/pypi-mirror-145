import os, pathlib
from rmlab.api.fetch.core import APIFetchCore
from rmlab.api.operations.simulation import APISimulation
from rmlab.api.upload.core import APIUploadCore
from rmlab.api.upload.parametric.filters import APIUploadParametric
from rmlab.api.upload.parametric.customers import APIUploadCustomersModels
from rmlab.api.upload.parametric.pricing import APIUploadPricingModels

from rmlab._data.enums import ScenarioDayStatus, ScenarioState

_DataSamplesPath = (
    str(pathlib.Path(os.path.realpath(__file__)).parent.parent) + "/data_samples/"
)


class APISimulationUpload(
    APISimulation,
    APIFetchCore,
    APIUploadCore,
    APIUploadParametric,
    APIUploadCustomersModels,
    APIUploadPricingModels,
):
    pass


async def test_trigger():

    async with APISimulationUpload() as api:

        scen_id = api.scenarios[0]

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
            scen_id, _DataSamplesPath + "/basic/table.pfilter.json"
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

        (
            prev_dates,
            prev_items_count,
            prev_schedules_count,
            prev_flights_count,
        ) = await api.fetch_info(scen_id)

        assert all(
            [
                count > 0
                for key, count in prev_items_count.__dict__.items()
                if key != "id"
            ]
        )

        assert prev_dates.current == prev_dates.first_flight_load
        assert prev_dates.next == prev_dates.last_flight_departure
        assert prev_dates.state == ScenarioState.IN_PROGRESS
        assert prev_dates.day_status == ScenarioDayStatus.READY

        assert prev_schedules_count.past == 0
        assert prev_schedules_count.live > 0
        assert prev_schedules_count.pending > 0
        assert prev_schedules_count.total > 0

        assert prev_flights_count.past == 0
        assert prev_flights_count.live > 0
        assert prev_flights_count.pending > 0
        assert prev_flights_count.total > 0

        (
            dates,
            items_count,
            schedules_count,
            flights_count,
        ) = await api.trigger_simulation(scen_id)

        assert dates.current == dates.last_flight_departure
        assert dates.state == ScenarioState.FINISHED
        assert dates.day_status == ScenarioDayStatus.ENDED

        assert all(
            [
                count > 0
                for key, count in prev_items_count.__dict__.items()
                if key != "id"
            ]
        )

        # NOTE: Live flights/schedules can be greater than 0 because non-zero number of flights departed on current
        assert flights_count.live >= 0
        assert flights_count.pending == 0
        assert flights_count.total >= flights_count.past

        assert schedules_count.live >= 0
        assert schedules_count.pending == 0
        assert schedules_count.total >= schedules_count.past
