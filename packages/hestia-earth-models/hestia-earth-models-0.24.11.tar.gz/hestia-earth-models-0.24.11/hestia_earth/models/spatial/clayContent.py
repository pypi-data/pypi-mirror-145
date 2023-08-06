from functools import reduce
from typing import List
from hestia_earth.schema import MeasurementStatsDefinition
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement, measurement_value
from .utils import MAX_AREA_SIZE, download, find_existing_measurement, has_geospatial_data, should_download
from . import MODEL

TERM_ID = 'clayContent,sandContent,siltContent'
TERM_IDS = {
    'clayContent': 'T_CLAY',
    'sandContent': 'T_SAND',
    'siltContent': None
}
EE_PARAMS = {
    'ee_type': 'raster',
    'reducer': 'mean',
    'fields': 'mean'
}
BIBLIO_TITLE = 'The harmonized world soil database. verson 1.0'


def _measurement(term_id: str, value: int):
    measurement = _new_measurement(term_id, MODEL, BIBLIO_TITLE)
    measurement['value'] = [value]
    measurement['depthUpper'] = 0
    measurement['depthLower'] = 30
    measurement['statsDefinition'] = MeasurementStatsDefinition.SPATIAL.value
    return measurement


def _download(site: dict, term_id: str, collection: str):
    value = download(
        term_id,
        site,
        {
            **EE_PARAMS,
            'collection': collection
        }
    ).get(EE_PARAMS['reducer'])
    return None if value is None else round(value, 2)


def _run_content(site: dict, term_id: str, collection: str):
    value = find_existing_measurement(TERM_ID, site) or _download(site, term_id, collection)
    return [_measurement(term_id, value)] if value else []


def _run_all(site: dict, models: List[str]):
    other_models = list(filter(lambda model: TERM_IDS[model] is not None, models))
    measurements = reduce(
        lambda prev, term_id: prev + _run_content(site, term_id, TERM_IDS[term_id]),
        other_models,
        []
    )
    # if we calculated all but 1 model, it can be calculated without querying GEE
    model_keys = _missing_terms(measurements)
    return measurements + (_run_single(measurements, model_keys[0]) if len(model_keys) == 1 else [])


def _run_single(measurements: list, model: str):
    other_models = list(TERM_IDS.keys())
    other_models.remove(model)
    value = reduce(
        lambda prev, curr: prev - measurement_value(find_term_match(measurements, curr, {})),
        other_models,
        100
    )
    return [_measurement(model, value)]


def _missing_term(measurement: dict):
    return measurement is None or any([
        measurement.get('value') is None,
        measurement.get('value') == []
    ])


def _missing_terms(measurements: list):
    return list(filter(
        lambda term_id: _missing_term(find_term_match(measurements, term_id, None)),
        list(TERM_IDS.keys())
    ))


def _run(site: dict, terms: list):
    measurements = site.get('measurements', [])
    return _run_single(measurements, terms[0]) if len(terms) == 1 else _run_all(site, terms)


def _should_run(site: dict):
    geospatial_data = has_geospatial_data(site)
    below_max_area_size = should_download(site)
    missing_terms = _missing_terms(site.get('measurements', []))
    has_missing_texture = len(missing_terms) > 0

    should_run = all([geospatial_data, below_max_area_size, has_missing_texture])

    for term in missing_terms:
        logRequirements(model=MODEL, term=term,
                        geospatial_data=geospatial_data,
                        max_area_size=MAX_AREA_SIZE,
                        below_max_area_size=below_max_area_size,
                        has_missing_texture=has_missing_texture)
        logShouldRun(MODEL, term, should_run)

    return should_run, missing_terms


def run(site: dict):
    should_run, missing_terms = _should_run(site)
    return _run(site, missing_terms) if should_run else []
