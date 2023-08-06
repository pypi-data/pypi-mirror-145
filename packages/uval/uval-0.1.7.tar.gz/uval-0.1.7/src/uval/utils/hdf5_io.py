# -*- coding: utf-8 -*-
"""This module provides functions to read and write uval HDF5 files.
For a format specification, have a look at `hdf5_format.py`
"""

import getpass  # type: ignore
import os  # type: ignore
import socket  # type: ignore
from abc import ABC  # type: ignore
from datetime import datetime, timezone  # type: ignore
from typing import Optional, Union  # type: ignore

import h5py  # type: ignore
from h5py import Group as H5Group  # type: ignore

from uval.utils.hdf5_format import *  # type: ignore
from uval.utils.log import logger  # type: ignore


class UvalHdfFile(ABC):
    def __init__(self, filepath: str, mode: str = "r"):
        self.filepath = filepath
        self.h5 = None
        self.file_mode = mode


class UvalHdfFileInput(UvalHdfFile):
    """A class to manage, read from a single uval-specific HDF5 file.
    The file on disk will not be held open by default.
    Every operation will open and close the file.
    If a bunch of operations is executed in a row and the file shall be held open, use
    a with-context on the UvalHdfFile object.
    """

    def __init__(self, filepath: str):
        super().__init__(filepath, "r")

        """Keeps track of nested with-statements.
           File will only be closed after exiting the last with-block"""
        self.context_counter = 0

    def __enter__(self):
        """
            Called on `with uval_file_obj:` to ensure the file is open.
            This is also used internally by the other member functions.
        Returns:
            The self object
        """
        self.context_counter += 1
        if self.h5 is None:
            try:
                self.h5 = h5py.File(self.filepath, self.file_mode)
            except OSError as err:
                logger.error(f"OS error '{err}' occurred while reading file: {self.filepath}")
                self.h5 = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the h5 file on disk is closed when we leave the with-context"""
        self.context_counter -= 1

        if self.context_counter == 0 and self.h5 is not None:
            self.h5.close()
            self.h5 = None

    def is_closed(self):
        """Checks if the file is closed or not initialized"""
        return not self.h5.__bool__()

    def _join_path(self, *args) -> str:
        """
            joins multiple elements of an HDF5 group or dataset path to one string.
        Examples:
            ["root", "some/other", "field"] would map to "root/some/other/field"
        Args:
            *args: The elements to be joined

        Returns:
            The joined input elements as a string
        """

        return "/".join(args)

    def _convert_read(self, item: object):
        """
            Takes a data field read from an HDF5 file and makes sure it's in the right format,
            to pass it to python. Bytes for example will be decoded to unicode strings.
        Args:
            item: the object to be decoded after reading

        Returns:
            The decoded object to pass to python
        """

        if isinstance(item, bytes):
            return item.decode()
        else:
            return item

    def _read_listgroup_to_dict(
        self, listgroup: str, listitem_fields: Union[dict, List[str], str], start_path: str = ""
    ) -> Optional[list]:
        try:
            list_keys = self.h5[self._join_path(start_path, listgroup)].keys()  # type: ignore
        except (TypeError, KeyError):
            return None

        return [
            self._read_to_dict(listitem_fields, start_path=self._join_path(start_path, listgroup, list_key))
            for list_key in list_keys
        ]

    def _read_dictgroup_to_dict(
        self, dictgroup: str, dictitem_fields: Union[dict, List[str], str], start_path: str = ""
    ) -> Optional[dict]:
        try:
            dict_keys = self.h5[self._join_path(start_path, dictgroup)].keys()  # type: ignore
        except (TypeError, KeyError):
            return None

        return {
            dict_key: self._read_to_dict(dictitem_fields, start_path=self._join_path(start_path, dictgroup, dict_key))
            for dict_key in dict_keys
        }

    def _read_to_dict(self, fields: Union[dict, List[str], str], start_path: str = "") -> Optional[dict]:
        """
            Extract (copy) all the data for the given fields from the HDF5 file, and return them in a dictionary.
            This is done recursively.

        Args:
            fields: The fields in HDF5 file to extract data from
            start_path: The start path to start extracting requested data from
        Returns:
            A dictionary of data in the requested filed
        """
        result = {}
        with self:
            if start_path:
                try:
                    # Let's check if the start_path exists within the HDF5 file.
                    # If not, we return None
                    self.h5[start_path]  # type: ignore
                except (TypeError, KeyError):
                    return None

            if isinstance(fields, str):
                # Single string (reading one data set) will be transformed to a list with one element
                fields = [fields]

            if isinstance(fields, list):
                # To not replicate reading code, transform list into dict with None-values
                fields = {k: None for k in fields}

            if isinstance(fields, dict):
                for key, subfields in fields.items():
                    if subfields is None:
                        # In this case, the key is the name of the dataset to read
                        try:
                            result[key] = self._convert_read(
                                self.h5[self._join_path(start_path, key)][()]  # type: ignore
                            )  # type: ignore
                        except KeyError:
                            # Don't set if not available
                            # Don't throw an error either
                            pass
                    else:
                        cur_result = self._read_to_dict(subfields, start_path=self._join_path(start_path, key))
                        if cur_result is not None:
                            result[key] = cur_result

        return result

    def _read_to_dict_outer(self, fields: Union[dict, List[str], str], start_path: str = "") -> Optional[dict]:
        """
            A wrapper around _read_to_dict, which leaves away the first hierarchy level of the returned dict.
            That means, if you request fields like {'root': {'A': None, 'B': None}}, it would directly return the
            inner dict with A and B and it's values, but not the root node.

        Args:
            fields: The requested fields to be read from the HDF5 file
            start_path: The field to start reading from it

        Returns:
            The results read from the HDF5 file in a dictionary
        """
        if isinstance(fields, dict):
            assert len(fields.keys()) == 1

        result = self._read_to_dict(fields, start_path)
        if result:
            return result[next(iter(fields.keys()))]  # type: ignore

        return result

    def file_meta(self):
        return self._read_to_dict_outer(
            {
                GROUP_FILE_META: {
                    DSET_HOST_NAME: None,
                    DSET_USER_NAME: None,
                    DSET_DT_GENERATED: None,
                    DSET_DET_VERSION: None,
                }
            }
        )

    def volume_meta(self, include_caches=False):
        """
            The metadata information regarding the ct 3d image.
            Please refer to UVal hdf5 format.
        Args:
            include_caches: Whether to include the cached data or not

        Returns:
            None
        """
        if include_caches:
            return self._read_to_dict_outer(
                {
                    GROUP_VOLUME_META: {
                        DSET_ID: None,
                        DSET_FILE_MD5: None,
                        DSET_FULL_SHAPE: None,
                        DSET_IS_CROPPED: None,
                        DSET_ROI_SHAPE: None,
                        DSET_ROI_START: None,
                        GROUP_CACHE: {DSET_PROJECTION_X, DSET_PROJECTION_Y, DSET_PROJECTION_Z},
                    }
                }
            )
        else:
            return self._read_to_dict_outer(
                {
                    GROUP_VOLUME_META: {
                        DSET_ID: None,
                        DSET_FILE_MD5: None,
                        DSET_FULL_SHAPE: None,
                        DSET_IS_CROPPED: None,
                        DSET_ROI_SHAPE: None,
                        DSET_ROI_START: None,
                    }
                }
            )

    def volume(self):
        """
            The ct 3d volume stored in hdf5 file
            Please refer to UVal hdf5 format.
        Returns:
            None
        """
        return self._read_to_dict_outer(DSET_VOLUME)

    def ground_truth(self, include_masks=False, include_caches=False):
        """
            A list of 3d groundtruth data belonging to a ct image
            Please refer to UVal hdf5 format.
        Args:
            include_masks: To include 3d masks while reading or not
            include_caches: To include cached data while reading ot not

        Returns:
            None
        """
        item_descriptor = {
            DSET_CLASS_NAME: None,
            DSET_TARGET_ID: None,
            DSET_ROI_START: None,
            DSET_ROI_SHAPE: None,
        }
        if include_masks:
            item_descriptor.update({DSET_MASK: None})

        if include_caches:
            item_descriptor.update({GROUP_CACHE: {DSET_PROJECTION_X, DSET_PROJECTION_Y, DSET_PROJECTION_Z}})

        return self._read_dictgroup_to_dict(DICTGROUP_GROUNDTRUTH, item_descriptor)

    def detections(self, include_masks=False, include_caches=False):
        """
            A list of detected areas in the ct image
            Please refer to UVal hdf5 format.
        Args:
            include_masks: To include 3d masks while reading or not
            include_caches: To include cached data while reading ot not

        Returns:
            None
        """
        item_descriptor = {
            DSET_CLASS_NAME: None,
            DSET_ROI_START: None,
            DSET_ROI_SHAPE: None,
            DSET_SCORE: None,
        }
        if include_masks:
            item_descriptor.update({DSET_MASK: None})

        if include_caches:
            item_descriptor.update({GROUP_CACHE: {DSET_PROJECTION_X, DSET_PROJECTION_Y, DSET_PROJECTION_Z}})

        return self._read_listgroup_to_dict(LISTGROUP_DETECTIONS, item_descriptor)

    def read_all_fields(self) -> dict:
        """
            Reads all the existing fields in h5 file
        Returns:
            All the groups in a dictionary
        """
        return {
            GROUP_FILE_META: self.file_meta(),
            GROUP_VOLUME_META: self.volume_meta(),
            DSET_VOLUME: self.volume(),
            DICTGROUP_GROUNDTRUTH: self.ground_truth(),
            LISTGROUP_DETECTIONS: self.detections(),
        }


class UvalHdfFileOutput(UvalHdfFile):
    """A class to manage, write to a single uval-specific HDF5 file.
    The file on disk will not be held open by default.
    Every operation will open and close the file.
    If a bunch of operations is executed in a row and the file shall be held open, use
    a with-context on the UvalHdfFile object.
    """

    _volume: Optional[np.ndarray]
    _volume_meta: Optional[dict]
    _groundtruth: Optional[dict]
    _detections: Optional[list]
    _file_meta: Optional[dict]

    # Always keeps all things in memory before writing
    def __init__(self, filepath: str, copy_from_input: Optional[UvalHdfFileInput] = None):
        super().__init__(filepath, "w")
        if copy_from_input:
            self.read_all_from(copy_from_input)
        else:
            self._volume = None
            self._volume_meta = None
            self._groundtruth = None
            self._detections = None
            self._file_meta = None

    def __enter__(self):
        """
            For the output class, we only actually write when done, not at this point.
        Returns:
            Self object of type UvalHdfFileOutput
        """
        if not os.access(os.path.abspath(os.path.dirname(self.filepath)), os.W_OK):
            raise IOError(f"Cannot write to file '{self.filepath}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """We are done, we can write the file now, if no exception occurred."""
        if exc_type is None:
            # Do not write if an exception occurred
            self.write()

    def _on_close(self):
        """Before closing, write the changes"""
        self.write()

    def _write_dict_to_group(self, h5group: H5Group, fields: dict):
        """In the HDF5 file, create groups and field at given start_path, containing the data from fields.

        Args:
            h5group: The HDF5 group to write the filed into
            fields: A nested dictionary representing the data to be written
        Returns:
            None
        """

        # The file needs to be writable
        assert self.file_mode == "w"

        for k, v in fields.items():
            if isinstance(v, dict):
                h5group.create_group(k)
                self._write_dict_to_group(h5group[k], v)
            else:
                h5group.create_dataset(k, data=v)

    def write(self):
        """
            Explicitly call this method to write the file. However, changes will automatically
            be written when the file is closed.
        Returns:
            None
        """

        # Check for meta data
        if self._volume_meta is None:
            raise ValueError(
                "No volume metadata was set before writing. " "Uval files always must contain volume metadata."
            )

        with h5py.File(self.filepath, "w") as f:
            # Write file meta data (This will always be generated here, cannot be set manually)
            group_file_meta = f.create_group(GROUP_FILE_META)
            group_file_meta.create_dataset(DSET_HOST_NAME, data=socket.gethostname())
            group_file_meta.create_dataset(DSET_USER_NAME, data=getpass.getuser())
            group_file_meta.create_dataset(
                DSET_DT_GENERATED, data=str(datetime.now(timezone.utc).astimezone().isoformat())
            )

            # As stated above, file_meta cannot be set manually - with one exception: det_version
            try:
                group_file_meta.create_dataset(DSET_DET_VERSION, data=self._file_meta[DSET_DET_VERSION])
            except (TypeError, KeyError):
                group_file_meta.create_dataset(DSET_DET_VERSION, data="not specified")

            # Write volume meta data
            check_volume_meta_fields(self._volume_meta, self._volume)
            group_volume_meta = f.create_group(GROUP_VOLUME_META)
            self._write_dict_to_group(group_volume_meta, self._volume_meta)

            # Write volume data if available
            if self._volume is not None:
                f.create_dataset(DSET_VOLUME, data=self._volume)

            # Write detections
            if self._detections:
                check_detection_fields(self._detections)
                listgroup_detections = f.create_group(LISTGROUP_DETECTIONS)
                for idx, detection in enumerate(self._detections):
                    group_detection = listgroup_detections.create_group(str(idx))
                    self._write_dict_to_group(group_detection, detection)

            # Write groundtruth:
            if self._groundtruth:
                check_groundtruth_fields(self._groundtruth)
                listgroup_groundtruth = f.create_group(DICTGROUP_GROUNDTRUTH)
                for label_name, gt in self._groundtruth.items():
                    group_gt = listgroup_groundtruth.create_group(str(label_name))
                    self._write_dict_to_group(group_gt, gt)

    def is_closed(self):
        """Checks if the file is closed or not initialized"""
        return not self.h5.__bool__()

    def read_all_from(self, input_file: UvalHdfFileInput) -> None:
        """Reading all the meta data included in another HDF5 file
        Args:
            input_file: HDF file to read from

        Returns:
            None
        """

        self._groundtruth = input_file.ground_truth()
        self._detections = input_file.detections()
        self._file_meta = input_file.file_meta()
        self._volume_meta = input_file.volume_meta()
        self._volume = input_file.volume()

    # File_meta
    @property
    def file_meta(self):
        raise IOError("This class should only be used to write, not to read a uval file")

    @file_meta.setter
    def file_meta(self, value: dict):
        self._file_meta = value

    @file_meta.deleter
    def file_meta(self):
        self._file_meta = None

    # Volume
    @property
    def volume(self):
        raise IOError("This class should only be used to write, not to read a uval file")

    @volume.setter
    def volume(self, value: np.ndarray):
        self._volume = value

    @volume.deleter
    def volume(self):
        self._volume = None

    # Volume meta
    @property
    def volume_meta(self):
        raise IOError("This class should only be used to write, not to read a uval file")

    @volume_meta.setter
    def volume_meta(self, value: dict):
        self._volume_meta = value

    @volume_meta.deleter
    def volume_meta(self):
        self._volume_meta = None

    # Detections
    @property
    def detections(self):
        raise IOError("This class should only be used to write, not to read a uval file")

    @detections.setter
    def detections(self, value: list):
        self._detections = value

    @detections.deleter
    def detections(self):
        self._detections = None

    # Groundtruth
    @property
    def groundtruth(self):
        raise IOError("This class should only be used to write, not to read a uval file")

    @groundtruth.setter
    def groundtruth(self, value: list):
        self._groundtruth = value  # type: ignore

    @groundtruth.deleter
    def groundtruth(self):
        self._groundtruth = None
