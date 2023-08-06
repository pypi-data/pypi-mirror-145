from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.spatial.clayContent import MODEL, TERM_IDS, _should_run, _run_single, run

class_path = f"hestia_earth.models.{MODEL}.clayContent"
fixtures_folder = f"{fixtures_path}/{MODEL}/clayContent"


@patch(f"{class_path}.should_download", return_value=True)
@patch(f"{class_path}.has_geospatial_data")
def test_should_run(mock_has_geospatial_data, *args):
    mock_has_geospatial_data.return_value = True

    site = {}
    # with 1 measurement with model => run
    measurement = {
        'term': {
            '@id': list(TERM_IDS.keys())[0]
        },
        'value': [10]
    }
    site['measurements'] = [measurement]
    should_run, *args = _should_run(site)
    assert should_run is True

    # with 3 measurements with model => NO run
    site['measurements'].append({
        'term': {
            '@id': list(TERM_IDS.keys())[1]
        },
        'value': [10]
    })
    site['measurements'].append({
        'term': {
            '@id': list(TERM_IDS.keys())[2]
        },
        'value': [10]
    })
    should_run, *args = _should_run(site)
    assert not should_run


@patch(f"{class_path}.find_existing_measurement", return_value=None)
@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
def test_run_single(*args):
    model = list(TERM_IDS.keys())[0]
    measurements = [{
        'term': {
            '@id': list(TERM_IDS.keys())[1]
        },
        'value': [20]
    }, {
        'term': {
            '@id': list(TERM_IDS.keys())[2]
        },
        'value': [30]
    }]
    measurement = _run_single(measurements, model)[0]
    assert measurement.get('value') == [50]


@patch(f"{class_path}.find_existing_measurement", return_value=None)
@patch(f"{class_path}.download", return_value={})
def test_run(mock_download, *args):
    with open(f"{fixtures_path}/{MODEL}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    run(site)
    assert mock_download.call_count == 2
