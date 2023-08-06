# type: ignore
"""This module defines the abstract base class for a stage.
A stage is one step of an evaluation pipeline to be executed, for example
converting detections from one format to another.
"""

import functools
from typing import Callable

from uval.utils.log import logger


def uval_stage(func: Callable):
    """This decorator has to be applied to every stage that is defined.
    We can use this to log the start and end of stages, handle caching etc."""

    @functools.wraps(func)
    def wraps_stage(*args, **kwargs):
        logger.info(f"Starting stage '{func.__qualname__}'")
        result = func(*args, **kwargs)
        logger.info(f"Stage '{func.__qualname__}' done")
        return result

    return wraps_stage
