import os
from datetime import datetime
from os import path

import randomname  # type: ignore
from fvcore.common.config import CfgNode as CN  # type: ignore

# -----------------------------------------------------------------------------
# Config definition
# -----------------------------------------------------------------------------
CPUS = os.cpu_count() if os.cpu_count() else 1
UVAL_DIR = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
_C = CN()

_C.ENV = CN()
_C.ENV.CACHE_FOLDER = UVAL_DIR

_C.DATA = CN()
_C.DATA.PATH = path.join(UVAL_DIR, "data", "hdf5")
_C.DATA.IGNORE_MISSING_FILES = False
_C.DATA.MAX_THREADS = CPUS

_C.DATA_SPLIT = CN()
_C.DATA_SPLIT.YAML = path.join(UVAL_DIR, "data", "datasplit", "uval_ds.yaml")
_C.DATA_SPLIT.SUBSET = ["train", "test"]


_C.METRICS = CN()
# f-{factor] score
_C.METRICS.FACTOR = 1
_C.METRICS.IOU_THRESHOLD = 0.3
_C.METRICS.IOU_RANGE = (0,)
_C.METRICS.MAX_PROCESSES = CPUS
_C.METRICS.CONFIDENCE_THRESHOLD = 0.6
_C.METRICS.AP_METHOD = "EveryPointInterpolation"
tt = datetime.now()

_C.OUTPUT = CN()
_C.OUTPUT.PATH = path.abspath(path.join(UVAL_DIR, "output", tt.strftime("%Y%m%d%H%M%S")))
_C.OUTPUT.TITLE = randomname.get_name()
_C.OUTPUT.TEMPLATES_PATH = path.abspath(path.join(UVAL_DIR, "src", "uval", "templates"))
_C.OUTPUT.CONFIG_FILE = "config.yaml"
_C.OUTPUT.REPORT_FILE = "report.html"
_C.OUTPUT.METRICS_FILE = "metrics.pickle"
_C.OUTPUT.DATASET_OVERVIEW_FILE = "dataset_overview.csv"
