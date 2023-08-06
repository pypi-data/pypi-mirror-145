# -*- coding: utf-8 -*-

import importlib.util
import unittest

from uval.utils.log import RootLogger


class TestLogMethods(unittest.TestCase):
    def test_root_logger_init(self):
        root_logger = RootLogger()
        self.assertEqual(len(root_logger.root_logger.handlers), 1)
        self.assertEqual(root_logger.root_logger.level, 10)

    @unittest.skip("Not used for now")
    def test_load_uval_script(self):
        spec = importlib.util.spec_from_file_location("a_b", r"../stages/stage.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.__name__, "a_b")
        self.assertEqual(mod.__sizeof__(), 56)


if __name__ == "__main__":
    unittest.main()
