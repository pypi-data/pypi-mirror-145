# -*- coding: utf-8 -*-


class Hdf5Virtual:
    """
    This module provides the class Hdf5Virtual which represents a reference to an Hdf5 file
    that actually resides on disk somewhere. It keeps meta data and other low-storage information in memory.
    When trying to access larger parts of the file, like volume, masks or projections, it accesses the actual file.
    """

    def __init__(self):
        msg = f"Method '{print.__name__}' not implemented in class '{self.__class__}'."
        raise NotImplementedError(msg)
