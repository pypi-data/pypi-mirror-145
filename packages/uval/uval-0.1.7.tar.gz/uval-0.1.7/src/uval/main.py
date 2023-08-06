import hashlib
import pickle
from os import path

from rich.console import Console
from rich.traceback import install

from uval import *
from uval.stages.diff_reporter import DiffReporter
from uval.utils.log import logger
from uval.utils.yaml_io import load_yaml_data

console = Console()
install()


def main():
    parser = default_argument_parser()
    args = parser.parse_args()
    print("Command Line Args:", args)

    cfgs = setup_from_args(args)
    for cfg in cfgs:
        single(cfg)

    if len(cfgs) > 1:
        print("initiating the generation of a differential report...")
        # the contents of the dataset and the splits should match
        # otherwise comparison is meaningless
        # the metrics should also match
        md5_hash = {
            hashlib.md5(
                bytes(
                    str(dict(cfg.METRICS).pop("MAX_PROCESSES"))
                    + "".join(cfg.DATA_SPLIT.SUBSET)
                    + str(load_yaml_data(cfg.DATA_SPLIT.YAML)),
                    "UTF-8",
                )
            ).digest()
            for cfg in cfgs
        }

        if not len(set(md5_hash)) == 1:
            logger.warning("UVAL proudly refuses to compare Apples and Oranges!")
        else:
            logger.debug("The two datasets appear to be perfect matches")
            results = []
            for cfg in cfgs:
                filename = path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.METRICS_FILE)
                with open(filename, "rb") as f:
                    results.append(pickle.load(f))
        print("loaded")
        reporter = DiffReporter(results)
        reporter.run()


def single(cfg):
    if path.isfile(path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.METRICS_FILE)):
        print("metrics pickle already exists. skipping the evaluation...")
        return
    print(cfg)
    ctx = get_context(cfg.DATA.MAX_THREADS)
    ctx.set_cache_folder(cfg.ENV.CACHE_FOLDER)

    with ctx.cached():
        dataset = load_datasplit(cfg.DATA_SPLIT.YAML, cfg.DATA_SPLIT.SUBSET, output=cfg.OUTPUT)
        hdf5_detections, hdf5_groundtruth, soc_data = load_evaulation_files(
            cfg.DATA.PATH, dataset=dataset, max_workers=cfg.DATA.MAX_THREADS
        )

        supported_dataset = support_dataset_with_file_paths(hdf5_groundtruth, hdf5_detections, soc_data)
        evaluator = Metrics(supported_dataset, cfg.METRICS, cfg.OUTPUT)
        evaluator.evaluate()


if __name__ == "__main__":
    main()
