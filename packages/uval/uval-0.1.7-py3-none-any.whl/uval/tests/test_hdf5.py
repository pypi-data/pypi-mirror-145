# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

import h5py  # type: ignore
import numpy as np

from uval.utils.hdf5_format import DICTGROUP_GROUNDTRUTH, GROUP_FILE_META, GROUP_VOLUME_META, LISTGROUP_DETECTIONS
from uval.utils.hdf5_io import UvalHdfFileInput, UvalHdfFileOutput

SAMPLE_H5 = os.path.join(os.path.dirname(__file__), "sample.h5")

SAMPLE_DATA_DICT = {
    GROUP_FILE_META: {"det_version": "20-99-05"},
    GROUP_VOLUME_META: {
        "id": "BAG",
        "file_md5": "1a3ef6",
        "full_shape": np.array([1, 3, 2]),
        "is_cropped": 1,
        "roi_start": np.array([0, 0, 0]),
        "roi_shape": np.array([620, 420, 300]),
    },
    LISTGROUP_DETECTIONS: [
        {
            "class_name": "knife",
            "roi_start": np.array([0, 0, 0]),
            "roi_shape": np.array([10, 11, 12]),
            "score": 0.95,
            "mask": np.random.randint(2, size=(3, 3, 3)).astype(np.uint8),
        },
        {
            "class_name": "blunt",
            "roi_start": np.array([0, 0, 0]),
            "roi_shape": np.array([10, 11, 12]),
            "score": 0.98,
            "mask": np.random.randint(2, size=(3, 3, 3)).astype(np.uint8),
        },
    ],
    DICTGROUP_GROUNDTRUTH: {
        "%_label_1": {
            "class_name": "knife",
            "target_id": "",
            "roi_start": np.array([0, 0, 0]),
            "roi_shape": np.array([10, 11, 12]),
            "mask": np.random.randint(2, size=(3, 3, 3)).astype(np.uint8),
        },
        "%_label_2": {
            "class_name": "blunt",
            "target_id": "",
            "roi_start": np.array([0, 0, 0]),
            "roi_shape": np.array([10, 11, 12]),
            "mask": np.random.randint(2, size=(3, 3, 3)).astype(np.uint8),
        },
    },
}


def populate_test_hdf(out_h5: UvalHdfFileOutput) -> None:
    """
        Populates the object in param with sample data by reference
    Returns:
        None
    """
    out_h5.file_meta = SAMPLE_DATA_DICT[GROUP_FILE_META]
    out_h5.volume_meta = SAMPLE_DATA_DICT[GROUP_VOLUME_META]
    out_h5.detections = SAMPLE_DATA_DICT[LISTGROUP_DETECTIONS]
    out_h5.groundtruth = SAMPLE_DATA_DICT[DICTGROUP_GROUNDTRUTH]


def write_sample_h5_file(h5_path: str):
    """
        Writes an hdf5 data using the sample data
    Args:
        h5_path: Filepath to write h5 file into

    Returns:
        True if the file is created
    """
    with UvalHdfFileOutput(h5_path) as out_h5_f:
        populate_test_hdf(out_h5_f)
    if not h5py.is_hdf5(h5_path):
        raise ValueError("Sample file is not a valid hdf5 file")
    return os.path.isfile(h5_path)


class Hdf5TestSuite(unittest.TestCase):
    def setUp(self):
        self.tempdir_object = tempfile.TemporaryDirectory()
        self.tempdir = self.tempdir_object.name
        self.temp_h5 = os.path.join(self.tempdir, "test.h5")

    def test_writing_empty_hdf5(self):
        self.assertFalse(os.path.isfile(self.temp_h5), "File was there before creating it")
        # No volume metadata is set
        with self.assertRaises(ValueError):
            with UvalHdfFileOutput(self.temp_h5) as out_f:
                self.assertFalse(os.path.isfile(self.temp_h5), "Could not create HDF5 file")
                self.assertTrue(out_f.is_closed())
                out_f.write()
                self.assertFalse(out_f.is_closed())
        # File should not exist
        with self.assertRaises(OSError):
            os.unlink(self.temp_h5)

    def test_writing_hdf5(self):
        self.assertFalse(os.path.isfile(self.temp_h5), "File was there before creating it")

        with UvalHdfFileOutput(self.temp_h5) as out_f:
            self.assertFalse(os.path.isfile(self.temp_h5), "Could not create HDF5 file")
            populate_test_hdf(out_f)

        # Now verify the contents
        with h5py.File(self.temp_h5, "r") as f:
            self.assertTrue(GROUP_FILE_META in f)

            # label_group = f[HDFSchema.LABEL_GROUP]
            # num_labels = label_group[HDFSchema.NUM_LABELS][()]

        # Check if we can remove the file (if this fails, the file may still be open although it shouldn't)
        os.unlink(self.temp_h5)

    def test_reading_hdf5_all_at_once(self):
        self.assertTrue(write_sample_h5_file(SAMPLE_H5), f"Could not create sample h5 file: {SAMPLE_H5}")
        with UvalHdfFileInput(SAMPLE_H5) as f:
            print(f.read_all_fields())
        os.unlink(SAMPLE_H5)

    def test_reading_hdf5_step_by_step(self):
        # Check if file is closed in between
        self.assertTrue(write_sample_h5_file(SAMPLE_H5), f"Could not create sample h5 file: {SAMPLE_H5}")
        h5_sample = UvalHdfFileInput(SAMPLE_H5)
        print(h5_sample.volume_meta())
        self.assertTrue(h5_sample.is_closed())
        print(h5_sample.file_meta())
        self.assertTrue(h5_sample.is_closed())
        self.assertRaises(TypeError, h5_sample.ground_truth())
        self.assertTrue(h5_sample.is_closed())
        os.unlink(SAMPLE_H5)

    def test_integration_write_then_read1(self):
        with UvalHdfFileOutput(SAMPLE_H5) as out_h5_f:
            populate_test_hdf(out_h5_f)
            self.assertTrue(out_h5_f.is_closed())
        with UvalHdfFileInput(SAMPLE_H5) as in_h5_f:
            print(in_h5_f.volume_meta())
            self.assertFalse(in_h5_f.is_closed())
            print(in_h5_f.detections())
            self.assertFalse(in_h5_f.is_closed())
            print(in_h5_f.ground_truth())
            self.assertFalse(in_h5_f.is_closed())
        os.unlink(SAMPLE_H5)

    def test_integration_write_then_read2(self):
        # Test initializing from sample.h5 and writing back identically (as-is)
        # Then read again and compare all fields
        with UvalHdfFileOutput(SAMPLE_H5) as out_h5_f:
            populate_test_hdf(out_h5_f)
            self.assertTrue(out_h5_f.is_closed())
        with UvalHdfFileInput(SAMPLE_H5) as in_h5_f:
            self.assertEqual(in_h5_f.file_meta()["det_version"], SAMPLE_DATA_DICT[GROUP_FILE_META]["det_version"])
            sample_meta = SAMPLE_DATA_DICT[GROUP_VOLUME_META]
            for key in sample_meta.keys():
                if isinstance(sample_meta[key], (np.ndarray, np.generic)):
                    self.assertEqual(in_h5_f.volume_meta()[key].tolist(), sample_meta[key].tolist())
                else:
                    self.assertEqual(in_h5_f.volume_meta()[key], sample_meta[key])
        os.unlink(SAMPLE_H5)


if __name__ == "__main__":
    unittest.main()
