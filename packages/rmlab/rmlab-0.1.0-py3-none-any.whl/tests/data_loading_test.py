import os, pathlib
from rmlab.api.fetch.core import APIFetchCore
from rmlab.api.fetch.parametric import APIFetchParametric
from rmlab.api.remove import APIRemove
from rmlab.api.upload.core import APIUploadCore
from rmlab.api.upload.parametric.filters import APIUploadParametric
from rmlab.api.upload.parametric.customers import APIUploadCustomersModels
from rmlab.api.upload.parametric.pricing import APIUploadPricingModels

from rmlab._version import __version__

_DataSamplesPath = (
    str(pathlib.Path(os.path.realpath(__file__)).parent.parent) + "/data_samples/"
)


class APIUploadRemove(
    APIUploadCore,
    APIUploadParametric,
    APIUploadCustomersModels,
    APIUploadPricingModels,
    APIFetchParametric,
    APIRemove,
):
    pass


async def test_upload_tables():

    async with APIUploadRemove() as api:

        scen_id = api.scenarios[0]

        await api.remove_data_full(scen_id=scen_id)

        await api.upload_customers_request_model(
            scen_id=scen_id,
            data_fn=_DataSamplesPath + "/basic/customers_request.poisson_bl1.json",
        )

        await api.upload_customers_choice_model(
            scen_id=scen_id,
            data_fn=_DataSamplesPath + "/basic/customers_choice.mnl_bl1.json",
        )

        await api.upload_pricing_range_model(
            scen_id=scen_id,
            data_fn=_DataSamplesPath + "/basic/pricing_range.sample.json",
        )

        await api.upload_pricing_behavior_model(
            scen_id=scen_id,
            data_fn=_DataSamplesPath + "/basic/pricing_behavior.sample.json",
        )

        await api.upload_pricing_optimizer_model(
            scen_id=scen_id,
            data_fn=_DataSamplesPath + "/basic/pricing_optimizer.sample.json",
        )

        await api.upload_parametric_filters(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.pfilter.json"
        )

        await api.upload_aircrafts(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.aircraft.csv"
        )

        await api.upload_airlines(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.airline.csv"
        )

        await api.upload_airports(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.airport.csv"
        )

        await api.upload_cities(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.city.csv"
        )

        await api.upload_countries(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.country.csv"
        )

        await api.upload_schedules(
            scen_id=scen_id, data_fn=_DataSamplesPath + "/basic/table.schedule.csv"
        )


class APIUploadFetchRemove(
    APIUploadCore,
    APIUploadParametric,
    APIUploadCustomersModels,
    APIUploadPricingModels,
    APIFetchCore,
    APIFetchParametric,
    APIRemove,
):
    pass


async def test_reset_upload_get():

    async with APIUploadFetchRemove() as api:

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
                _DataSamplesPath + "./basic/pricing_optimizer.sample.json"
            ],
        )

        await api.upload_parametric_filters(
            scen_id, data_fn=_DataSamplesPath + "./basic/table.pfilter.json"
        )

        # Upload core items to server
        await api.upload_batch_core(
            scen_id,
            aircraft_items_fn=_DataSamplesPath + "./basic/table.aircraft.csv",
            airline_items_fn=_DataSamplesPath + "./basic/table.airline.csv",
            airport_items_fn=_DataSamplesPath + "./basic/table.airport.csv",
            city_items_fn=_DataSamplesPath + "./basic/table.city.csv",
            country_items_fn=_DataSamplesPath + "./basic/table.country.csv",
            schedule_items_fn=_DataSamplesPath + "./basic/table.schedule.csv",
        )

        # ---- Assert retrieval of scenario info
        dates, bounded_count, schedules_count, flights_count = await api.fetch_info(
            scen_id
        )

        # ---- Assert all core bounded items are initialized
        arl_items = await api.fetch_airlines(scen_id)
        assert len(arl_items) > 0

        for arl in arl_items:
            arl_sectors_ids = await api.fetch_airline_sectors(scen_id, arl.id)
            assert len(arl_sectors_ids) > 0

            arl_citysectors_ids = await api.fetch_airline_citysectors(scen_id, arl.id)
            assert len(arl_citysectors_ids) > 0

            arl_routes_ids = await api.fetch_airline_routes(scen_id, arl.id)
            assert len(arl_routes_ids) > 0

            arl_cityroutes_ids = await api.fetch_airline_cityroutes(scen_id, arl.id)
            assert len(arl_cityroutes_ids) > 0

        arc_items = await api.fetch_aircrafts(scen_id)
        assert len(arc_items) > 0

        arp_items = await api.fetch_airports(scen_id)
        assert len(arp_items) > 0

        cnt_items = await api.fetch_countries(scen_id)
        assert len(cnt_items) > 0

        cty_items = await api.fetch_cities(scen_id)
        assert len(cty_items) > 0

        pfl_items = await api.fetch_parametric_filters(scen_id)
        assert len(pfl_items) > 0

        pmd_items = await api.fetch_parametric_models(scen_id)
        assert len(pmd_items) > 0

        # ---- Assert all derived items are initialized
        csc_items = await api.fetch_citysectors(scen_id)
        assert len(csc_items) > 0

        crt_items = await api.fetch_cityroutes(scen_id)
        assert len(crt_items) > 0

        sct_items = await api.fetch_sectors(scen_id)
        assert len(sct_items) > 0

        rte_items = await api.fetch_routes(scen_id)
        assert len(rte_items) > 0

        # ---- Assert all unbounded items are initialized (by citysector)
        for csc in csc_items:

            sch_ids = await api.fetch_schedules_ids(scen_id, citysector_id=csc.id)
            assert len(sch_ids) > 0

            sch_items = await api.fetch_schedules(
                scen_id, sch_ids, citysector_id=csc.id
            )
            assert len(sch_items) > 0

            flt_ids = await api.fetch_flights_ids(scen_id, citysector_id=csc.id)
            assert len(flt_ids) > 0

            flt_items = await api.fetch_flights(scen_id, flt_ids, citysector_id=csc.id)
            assert len(flt_items) > 0

        # ---- Assert all unbounded items are initialized (by sector)
        for sct in sct_items:

            sch_ids = await api.fetch_schedules_ids(scen_id, sector_id=sct.id)
            assert len(sch_ids) > 0

            sch_items = await api.fetch_schedules(scen_id, sch_ids, sector_id=sct.id)
            assert len(sch_items) > 0

            flt_ids = await api.fetch_flights_ids(scen_id, sector_id=sct.id)
            assert len(flt_ids) > 0

            flt_items = await api.fetch_flights(scen_id, flt_ids, sector_id=sct.id)
            assert len(flt_items) > 0
