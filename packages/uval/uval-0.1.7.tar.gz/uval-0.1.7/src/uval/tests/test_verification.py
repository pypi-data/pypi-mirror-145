# -*- coding: utf-8 -*-

import sys
import unittest
from os import path, unlink
from pprint import pprint

import numpy as np

from uval.tests.test_hdf5 import write_sample_h5_file
from uval.utils.hdf5_io import UvalHdfFileOutput
from uval.utils.hdf5_verification import verify_hdf5_files, verify_single_hdf5_file

# to let the unittest find the files using the relative path
current_dir = path.dirname(__file__)
sys.path.insert(0, current_dir)


class TestVerificationMethods(unittest.TestCase):
    def test_verify_multiple_h5_files(self):
        sample_files = [
            f"{current_dir}/../../../data/hdf5/detections/BAGGAGE_20171205_072023_012345.det.h5",
            f"{current_dir}/../../../data/hdf5/raw/BAGGAGE_20180320_080245_124166.gt.h5",
        ]
        for h5_file in sample_files:
            print(f"\nChecking {h5_file}:")
            problems = verify_single_hdf5_file(h5_file)
            self.assertEqual(len(problems), 0)

    def test_verify_sample_h5_files(self):
        problems_det = verify_hdf5_files(f"{current_dir}/../../../data/hdf5/detections")
        self.assertEqual(len(problems_det), 0)
        problems_raw = verify_hdf5_files(f"{current_dir}/../../../data/hdf5/raw")
        self.assertEqual(len(problems_raw), 0)

    def test_create_and_verify_voldata_h5_file(self):
        # Generating voldata file and checking it:
        test_file = "test.voldata.h5"
        with UvalHdfFileOutput(test_file) as outf:
            outf.file_meta = {"det_version": "20-99-05"}
            outf.volume_meta = {
                "id": "BAG",
                "file_md5": "1a3ef6",
                "full_shape": np.array([1, 3, 2]),
                "is_cropped": 1,
                "roi_start": np.array([0, 0, 0]),
                "roi_shape": np.array([620, 420, 300]),
            }
            outf.volume = np.zeros((1, 3, 2), dtype=np.uint16)
        print("\nChecking generated volcache file:")
        problems = verify_single_hdf5_file(test_file)
        self.assertEqual(len(problems), 0)
        unlink(test_file)

    def test_create_and_verify_full_h5_file(self):
        sample_name = "test.det.h5"
        self.assertTrue(write_sample_h5_file(sample_name), f"Could not create sample h5 file: {sample_name}")
        problems = verify_single_hdf5_file(sample_name)
        self.assertEqual(len(problems), 0)
        unlink(sample_name)

    def test_create_and_verify_h5_file_with_invalid_name(self):
        invalid_name = "test.h5"
        self.assertTrue(write_sample_h5_file(invalid_name), f"Could not create sample h5 file: {invalid_name}")
        problems = verify_single_hdf5_file(invalid_name)
        self.assertEqual(len(problems), 1)
        pprint(problems)
        unlink(invalid_name)


if __name__ == "__main__":
    unittest.main()
