import pickle
from os import path

from uval.config import default_argument_parser
from uval.config.config_utils import setup_from_args
from uval.main import single
from uval.stages.diff_reporter import DiffReporter

CONFIGS_PATH_1 = "./output/example/config.yaml,./output/example2/config.yaml"
CONFIGS_PATH_2 = "./output/example2/config.yaml,./output/example2/config.yaml"


"""
def test_generate_report(load_test_data):
    load_test_data.evaluate()
    assert path.isfile(path.join(load_test_data.output_path, load_test_data.report_file))
"""


def test_diffs():
    diffs(CONFIGS_PATH_1)
    diffs(CONFIGS_PATH_2)


def diffs(configs):
    parser = default_argument_parser()
    args = parser.parse_args(["--config-file", configs])
    # args = parser.parse_args()
    print("Command Line Args:", args)

    cfgs = setup_from_args(args)
    assert len(cfgs) == 2
    for cfg in cfgs:
        single(cfg)

    if len(cfgs) > 1:
        print("initiating the generation of a differential report...")
        # the contents of the dataset and the splits should match
        # otherwise comparison is meaningless
        # the metrics should also match

        results = []
        for cfg in cfgs:
            filename = path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.METRICS_FILE)
            with open(filename, "rb") as f:
                results.append(pickle.load(f))
        reporter = DiffReporter(results)
        reporter.run()
        assert path.isdir(reporter.output_path)
        assert path.isfile(path.join(reporter.output_path, reporter.report_file))
