import argparse
import os
from os import path

from uval.utils.log import logger


def default_argument_parser(epilog=None):
    """
    Create a parser with some common arguments used by uval users.
    Args:
        epilog (str): epilog passed to ArgumentParser describing the usage.
    Returns:
        argparse.ArgumentParser:
    """
    parser = argparse.ArgumentParser(
        epilog=epilog or """ Examples: None existent at the moment.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config-file", default="", metavar="FILE", help="path to config file or files, comma separated"
    )
    parser.add_argument(
        "opts",
        help="""
            Modify config options at the end of the command. For Yacs configs, use
            space-separated "PATH.KEY VALUE" pairs.
            For python-based LazyConfig, use "path.key=value".
        """.strip(),
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser


def get_cfg():
    """
    Get a copy of the default config.
    Returns:
        a Uval CfgNode instance.
    """
    from .defaults import _C

    return _C.clone()


def setup_from_args(args):
    """
    Create configs and perform basic setups.
    """
    cfgs = []
    config_files = args.config_file.split(",")
    if not config_files:
        cfg = get_cfg()
        cfg_process(cfg, args.opts)
        cfgs.append(cfg)

    for config_file in config_files:
        cfg = get_cfg()
        if path.isfile(config_file):
            cfg.merge_from_file(config_file)
        cfg_process(cfg, args.opts)
        cfgs.append(cfg)
    return cfgs


def cfg_process(cfg, opts):
    cfg.merge_from_list(opts)
    cfg.freeze()
    os.makedirs(cfg.OUTPUT.PATH, exist_ok=True)
    cfg_str = cfg.dump()
    with open(os.path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.CONFIG_FILE), "w") as f:
        f.write(cfg_str)
    logger.info(f"config file saved to {os.path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.CONFIG_FILE)}.")
