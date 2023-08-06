from hestia_earth.schema import IndicatorStatsDefinition

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, get_site, convert_value_from_cycle
from hestia_earth.models.utils.cycle import land_occupation_per_kg
from hestia_earth.models.utils.input import sum_input_impacts
from . import MODEL

TERM_ID_CYCLE = 'landOccupationDuringCycle'
TERM_ID_INPUTS = 'landOccupationInputsProduction'
TERM_ID = 'landOccupationDuringCycle,landOccupationInputsProduction'


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run_inputs(impact_assessment: dict, product: dict):
    cycle = impact_assessment.get('cycle', {})
    value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID_CYCLE))
    debugValues(nodel=MODEL, term=TERM_ID_INPUTS,
                value=value)
    return [] if value is None else [_indicator(TERM_ID_INPUTS, value)]


def _should_run(impact_assessment: dict):
    product = get_product(impact_assessment)
    cycle = impact_assessment.get('cycle', {})
    # need to set the site on the Cycle as land occupation needs to fetch some measurements
    cycle['site'] = get_site(impact_assessment)
    land_occupation_kg = land_occupation_per_kg(MODEL, TERM_ID_CYCLE, cycle, product)

    logRequirements(model=MODEL, term=TERM_ID_CYCLE,
                    land_occupation_kg=land_occupation_kg)

    should_run = land_occupation_kg is not None
    logShouldRun(MODEL, TERM_ID_CYCLE, should_run)

    should_run_inputs = all([product])
    logShouldRun(MODEL, TERM_ID_INPUTS, should_run_inputs)

    return should_run, should_run_inputs, land_occupation_kg, product


def run(impact_assessment: dict):
    should_run, should_run_inputs, land_occupation_kg, product = _should_run(impact_assessment)
    return (
        [_indicator(TERM_ID_CYCLE, land_occupation_kg)] if should_run else []
    ) + (
        _run_inputs(impact_assessment, product) if should_run_inputs else []
    )
