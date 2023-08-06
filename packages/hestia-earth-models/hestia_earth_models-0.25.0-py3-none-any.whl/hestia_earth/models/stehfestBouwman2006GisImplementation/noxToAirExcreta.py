from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.utils.cycle import get_excreta_N_total
from hestia_earth.models.utils.emission import _new_emission
from .noxToAirSoilFlux import _should_run, _get_value
from . import MODEL

TERM_ID = 'noxToAirExcreta'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, country_id: str, N_total: float):
    noxToAirSoilFlux = _get_value(country_id, N_total, TERM_ID)
    excreta_N_total = get_excreta_N_total(cycle)
    return [_emission(excreta_N_total * noxToAirSoilFlux / N_total)]


def run(cycle: dict):
    should_run, country_id, N_total, *args = _should_run(cycle, TERM_ID, TIER)
    return _run(cycle, country_id, N_total) if should_run else []
