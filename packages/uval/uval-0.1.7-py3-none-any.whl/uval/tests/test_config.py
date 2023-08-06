from os import path  # type: ignore

import pytest  # type: ignore

from uval.config import default_argument_parser  # type: ignore
from uval.config.config_utils import setup_from_args  # type: ignore


@pytest.fixture
def setup():
    """
    Create configs and perform basic setups.
    """
    parser = default_argument_parser()
    args = parser.parse_args()
    cfg = setup_from_args(args)
    if isinstance(cfg, list):
        return cfg[0]
    else:
        return cfg


def test_config(setup):
    assert path.isdir(setup.ENV.CACHE_FOLDER)
    assert path.isdir(setup.DATA.PATH)
    assert type(setup.DATA.IGNORE_MISSING_FILES) == bool
    assert path.isfile(setup.DATA_SPLIT.YAML)
    assert type(setup.DATA_SPLIT.SUBSET) == list and len(setup.DATA_SPLIT.SUBSET) >= 1
    assert type(setup.METRICS.FACTOR) == int and setup.METRICS.FACTOR >= 1
    assert type(setup.METRICS.IOU_THRESHOLD) == float and 0.0 <= setup.METRICS.IOU_THRESHOLD <= 1.0
    assert type(setup.METRICS.CONFIDENCE_THRESHOLD) == float and 0.0 <= setup.METRICS.CONFIDENCE_THRESHOLD <= 1.0
    assert setup.METRICS.AP_METHOD == "EveryPointInterpolation" or setup.METRICS.AP_METHOD == "ElevenPointInterpolation"

    assert path.isdir(setup.OUTPUT.PATH)
    assert path.isdir(setup.OUTPUT.TEMPLATES_PATH)
