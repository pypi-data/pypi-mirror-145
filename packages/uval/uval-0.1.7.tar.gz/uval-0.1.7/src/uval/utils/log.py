# -*- coding: utf-8 -*-
"""This utils module currently only provides logging functionality.
Once this grows to much, we will need to split it.
"""

import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("uval")


class RootLogger:
    """
    All the child logger messages will propagate through this root logger
    """

    def __init__(self, logging_level=logging.DEBUG):
        """
            The root logger will be configured but should never be used directly for logging
        Child loggers will propagate their messages up to the root logger
        Args:
            logging_level: The verbosity level of logger
        """

        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(logging_level)

        # The logging formats are currently not configurable
        self.stream_formatter = logging.Formatter(fmt="%(asctime)s %(name)s [%(levelname)s]: %(message)s")
        self.popup_formatter = logging.Formatter(fmt="%(name)s [%(levelname)s]: %(message)s")

        # Now set up our initial logging handlers
        self.set_up_handlers()

    def set_up_handlers(self):
        """
        Sets up Stream Handlers
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.stream_formatter)
        self.root_logger.handlers = [
            stream_handler,
        ]
