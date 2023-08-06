# -*- coding: utf-8 -*-
"""This module provides the Context class. The user of uval shall create a single instance
of this class and call all the stages as needed.

For an example on how to use this, please that a look at the examples folder.
"""

from contextlib import AbstractContextManager

_uval_instance = None


class Context:
    def __init__(self, max_workers=None):
        self.config = {"hdf5_io": {"num_threads": max_workers}}
        self._cached = False  # Set to true when in a cached context (with ctx.cached(): block)
        self.cache_folder = None
        self.cached_context_manager = CachedContextManager(self)

    def set_cache_folder(self, folder_path: str):
        self.cache_folder = folder_path

    def cached(self):
        if self.cache_folder is None:
            raise ValueError("Before using cached, you need to set a folder with `Context.set_cache_folder()`")
        return self.cached_context_manager


class CachedContextManager(AbstractContextManager):
    """This context manager will be returned by `Context.cached()` and can be used in a with
    statement. All"""

    _stream = None

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.entry_counter = 0

    def __enter__(self):
        self.entry_counter += 1
        self.ctx._cached = True

    def __exit__(self, exctype, excinst, exctb):
        self.entry_counter -= 1
        if self.entry_counter <= 0:
            self.entry_counter = 0
            self.ctx._cached = False


def get_context(max_workers):
    global _uval_instance
    if _uval_instance is None:
        _uval_instance = Context(max_workers)
    return _uval_instance
