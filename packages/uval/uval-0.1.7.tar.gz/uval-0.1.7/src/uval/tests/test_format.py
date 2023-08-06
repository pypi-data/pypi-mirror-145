# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from uval.tests.test_hdf5 import write_sample_h5_file
from uval.utils.hdf5_verification import *


class TestFormatMethods(unittest.TestCase):

    temp_h5_path = ""
    sample_h5 = None

    def __init__(self, *args, **kwargs):
        super(TestFormatMethods, self).__init__(*args, **kwargs)
        self.tempdir_object = tempfile.TemporaryDirectory()
        self.tempdir = self.tempdir_object.name
        self.temp_h5_path = os.path.join(self.tempdir, "test_format.h5")
        write_sample_h5_file(self.temp_h5_path)
        self.sample_h5 = UvalHdfFileInput(self.temp_h5_path)

    def __del__(self):
        if os.path.exists(self.temp_h5_path):
            os.unlink(self.temp_h5_path)

    def test_check_fields(self):
        with UvalHdfFileInput(self.temp_h5_path) as f:
            functions = [
                h5_check_file_meta_fields,
                h5_check_detection_fields,
                h5_check_groundtruth_fields,
                h5_check_volume_meta_fields,
            ]
            for func in functions:
                try:
                    func(f.h5)
                except ValueError:
                    self.fail(f"'{func}' raised ValueError unexpectedly!")

    def test_for_not_existing_fields(self):
        with UvalHdfFileInput(self.temp_h5_path) as f:
            self.assertRaises(ValueError, h5_check_volcache, f.h5)

    def test_verify_single_file(self):
        verify_single_hdf5_file(self.temp_h5_path)


if __name__ == "__main__":
    unittest.main()
