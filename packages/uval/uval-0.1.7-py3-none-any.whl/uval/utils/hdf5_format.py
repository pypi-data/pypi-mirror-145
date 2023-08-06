"""This module provides functions to read and write uval HDF5 files.
The supported HDF5 fields defined listed as yaml:

File name suggestion (let's keep tools functional even if names not complying)
- NAME.det.h5  (does not contain volume_data, groundtruth)
- NAME.gt.h5  (does not contain detections, volume_data)
- NAME.volcache.h5 (only volume_meta including volume projection cache)
- NAME.voldata.h5 (only volume_data)

# X, Y and Z axis
# Z-axis is belt direction (dir. of motion)
# Y-axis is vertical pointing up
# X-axis is point left when looking in belt motion direction

# Character set always UTF-8

file_meta:  # Always required
  host_name: "H5T_STRING"  # Host name of computer that generated the h5 file e.g. philscomputer
  user_name: "H5T_STRING"  # User name of user that generated the h5 file
  dt_generated: "H5T_STRING"  # ISO 8601 time and date of file creation (with timezone!)

volume_meta:  # Always available, not optional! (also for dets and gt)
  id: "H5T_STRING"  # e.g. BAGGAGE_20181122_081331_126018
  file_md5: "H5T_STRING"  # The checksum of the original ct volume file e.g. 686593fa1f05f610066129b72c62bfdd
  full_shape: INT (3) # Shape of full volume
  is_cropped: INT  # if 1, the data only contains the voxels within the roi
  roi_start: INT (3)
  roi_shape: INT (3) # Matches size of data if "is_cropped" is True
  cache:  # Optional
    projection_x: UINT8 RGB IMAGE  # Colored Matlum if possible, otherwise grayscale (R=G=B)
    projection_y: UINT8 RGB IMAGE
    projection_z: UINT8 RGB IMAGE

volume_data: "H5T_STD_U16LE"  # Optional (to save space, not contained in .dets.h5 and .gt.h5)

detections:  # list int-indexed as strings for each member (e.g. "0", "1", ..)
  class_name: "H5T_STRING"
  roi_start: INT (3)
  roi_shape: INT (3) # Same as size of mask if mask is available
  mask: "H5T_STD_U8LE"  # Optional (e.g. only bounding boxes)
  score: FLOAT
  cache:  # Optional
    density: FLOAT
    mass: FLOAT
    num_voxels: INT
    projection_x: UINT16 # Taking 3D mask with 1s and 0s, adding up along x axis (only y and z axis remain)
    projection_y: UINT16 # Taking 3D mask with 1s and 0s, adding up along y axis (only x and z axis remain)
    projection_z: UINT16 # Taking 3D mask with 1s and 0s, adding up along z axis (only x and y axis remain)

groundtruth:  # dict indexed by label id for each member
  class_name: "H5T_STRING"
  target_id: "H5T_STRING" # Formerly known as threat id
  roi_start: INT (3)
  roi_shape: INT (3) # Same as size of mask if mask is available
  mask: "H5T_STD_U8LE" # Optional (e.g. only bounding boxes)
  cache:  # Optional
    projection_x:  # As for detections
    projection_y:
    projection_z:


# 2D MASK projection to 1D
# X ---->
# 0 0 0 0 0 0 0  ^
# 0 1 0 1 0 0 0  |
# 0 1 1 1 1 0 0  |
# 0 0 1 1 0 0 0  Y
# 0 0 0 1 0 0 0

# 0 2 2 4 1 0 0  Projection (adding up)
# 0 1 1 1 1 0 0  Binary mask

# Proj along Y
"""

from enum import Enum
from typing import Any, Dict, List, Union

import numpy as np
from h5py import Dataset as H5Dataset  # type: ignore
from h5py import File as H5File  # type: ignore
from h5py import Group as H5Group  # type: ignore
from h5py import check_string_dtype

# Having all HDF5 internal group and field names as constants, helps preventing typos
# because a typo will make python complain on execution

GROUP_FILE_META = "file_meta"
GROUP_VOLUME_META = "volume_meta"
GROUP_CACHE = "cache"
LISTGROUP_DETECTIONS = "detections"
DICTGROUP_GROUNDTRUTH = "groundtruth"

DSET_HOST_NAME = "host_name"
DSET_USER_NAME = "user_name"
DSET_DT_GENERATED = "dt_generated"
DSET_DET_VERSION = "det_version"

DSET_ID = "id"
DSET_FILE_MD5 = "file_md5"

DSET_VOLUME = "volume"
DSET_FULL_SHAPE = "full_shape"
DSET_IS_CROPPED = "is_cropped"
DSET_ROI_START = "roi_start"
DSET_ROI_SHAPE = "roi_shape"
DSET_CLASS_NAME = "class_name"
DSET_SUBCLASS_NAME = "subclass_name"
DSET_TARGET_ID = "target_id"
DSET_MASK = "mask"
DSET_SCORE = "score"

DSET_PROJECTION_X = "projection_x"
DSET_PROJECTION_Y = "projection_y"
DSET_PROJECTION_Z = "projection_z"

DSET_DENSITY = "density"
DSET_MASS = "mass"
DSET_NUM_VOXELS = "num_voxels"


class FieldRequired(Enum):
    Required = 1
    Optional = 2


class ArrayReqs:
    """Used to represent requirements on an np.ndarray.
    Very similar to a type hint. So that `ArrayReqs(shape=(3,3,-1))` corresponds to a type hint like
    `np.ndarray[shape=(3,3,-1)]` where -1 indicates any size along that dimension.
    You can also use ArrayReqs(shape=3) to indicate the number of dimensions should be 3."""

    def __init__(self, shape=None, dtype=None):
        self.shape = shape
        self.dtype = np.dtype(dtype) if dtype else None

    def check(self, array: Union[np.ndarray, H5Dataset]) -> bool:
        if self.dtype and (array.dtype != self.dtype):
            return False

        if self.shape is None:
            return True

        if isinstance(self.shape, int):
            # Shape just is the number of dimensions
            # In this case, that's all we need to check and then return
            return self.shape == len(array.shape)
        else:
            # Shape is actually the shape (tuple with length for each dimension)
            if len(self.shape) != len(array.shape):
                return False

        # We now check every dimension for the length specified. -1 means any length is fine.
        for dim_idx in range(len(self.shape)):
            if self.shape[dim_idx] >= 0 and self.shape[dim_idx] != array.shape[dim_idx]:
                return False
        # If we passed all checks, the array is good
        return True

    def __repr__(self):
        if self.dtype is not None:
            return f"<ArrayReqs shape={self.shape} dtype={self.dtype}>"
        else:
            return f"<ArrayReqs shape={self.shape}>"


# The following definition of requirements is used to:
# 1. Verify parts of a file when reading it
# 2. Verify parts to be written to a file before writing them

format_requirements = {
    GROUP_FILE_META: (
        {
            DSET_HOST_NAME: (str, FieldRequired.Required),
            DSET_USER_NAME: (str, FieldRequired.Required),
            DSET_DT_GENERATED: (str, FieldRequired.Required),
            DSET_DET_VERSION: (str, FieldRequired.Required),
        },
        FieldRequired.Required,
    ),
    GROUP_VOLUME_META: (
        {
            DSET_ID: (str, FieldRequired.Required),
            DSET_FILE_MD5: (str, FieldRequired.Required),
            DSET_FULL_SHAPE: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_IS_CROPPED: (int, FieldRequired.Required),
            DSET_ROI_START: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_ROI_SHAPE: (ArrayReqs((3,)), FieldRequired.Required),
            GROUP_CACHE: (
                {
                    DSET_PROJECTION_X: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Y: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Z: (np.ndarray, FieldRequired.Required),
                },
                FieldRequired.Optional,
            ),
        },
        FieldRequired.Required,
    ),
    DSET_VOLUME: (ArrayReqs(3, dtype=np.uint16), FieldRequired.Optional),
    LISTGROUP_DETECTIONS: (
        {
            DSET_CLASS_NAME: (str, FieldRequired.Required),
            DSET_SUBCLASS_NAME: (str, FieldRequired.Optional),
            DSET_ROI_START: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_ROI_SHAPE: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_MASK: (np.ndarray, FieldRequired.Optional),
            DSET_SCORE: (float, FieldRequired.Required),
            GROUP_CACHE: (
                {
                    DSET_DENSITY: (float, FieldRequired.Optional),
                    DSET_MASS: (float, FieldRequired.Optional),
                    DSET_NUM_VOXELS: (int, FieldRequired.Optional),
                    DSET_PROJECTION_X: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Y: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Z: (np.ndarray, FieldRequired.Required),
                },
                FieldRequired.Optional,
            ),
        },
        FieldRequired.Optional,
    ),
    DICTGROUP_GROUNDTRUTH: (
        {
            DSET_CLASS_NAME: (str, FieldRequired.Required),
            DSET_SUBCLASS_NAME: (str, FieldRequired.Optional),
            DSET_TARGET_ID: (str, FieldRequired.Required),
            DSET_ROI_START: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_ROI_SHAPE: (ArrayReqs((3,)), FieldRequired.Required),
            DSET_MASK: (np.ndarray, FieldRequired.Optional),
            GROUP_CACHE: (
                {
                    DSET_PROJECTION_X: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Y: (np.ndarray, FieldRequired.Required),
                    DSET_PROJECTION_Z: (np.ndarray, FieldRequired.Required),
                },
                FieldRequired.Optional,
            ),
        },
        FieldRequired.Optional,
    ),
}


def check_dataset_type(dataset: object, type_descriptor) -> bool:
    """Check for a single dataset (a python value or H5Dataset) if it matches the type requirement."""
    # Find type kind of given data
    # (https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html#numpy.dtype.kind)
    if isinstance(dataset, H5Dataset):
        type_kind = dataset.dtype.kind
        if type_kind == "O" and check_string_dtype(dataset.dtype):
            type_kind = "S"  # It's a string, although technically not like numpy type 'S'
            # In the future we might also want to check whether its utf-8 and variable length
            # For that see https://docs.h5py.org/en/stable/special.html#variable-length-strings
    elif isinstance(dataset, str):
        type_kind = "S"
    elif isinstance(dataset, bool):
        type_kind = "b"
    elif isinstance(dataset, int):
        type_kind = "i"
    elif isinstance(dataset, float):
        type_kind = "f"
    elif isinstance(dataset, np.ndarray):
        type_kind = "nd"
    else:
        type_kind = "<None>"

    dataset_is_array = hasattr(dataset, "shape") and len(dataset.shape) > 0
    # Now check type descriptor against that type
    if isinstance(type_descriptor, ArrayReqs):
        if not dataset_is_array:
            # This is not an array
            return False
        return type_descriptor.check(dataset)
    elif type_descriptor is str:
        return type_kind in "SU" and not dataset_is_array
    elif type_descriptor is int:
        return type_kind in "iu" and not dataset_is_array
    elif type_descriptor is bool:
        return type_kind == "b" and not dataset_is_array
    elif type_descriptor is float:
        return type_kind == "f" and not dataset_is_array
    elif type_descriptor is np.ndarray:
        return type_kind == "nd" or dataset_is_array
    else:
        raise NotImplementedError(f"Type checking for {type_descriptor} not supported. Please implement it.")


def check_fields(to_check: Union[dict, H5Group], requirements: Union[Dict[Any, Any], Any], base_name: str = ""):
    """Checks a dict (group) or value (dataset) against requirements. Fields may be required or optional.
    Additional unknown fields will also result in a failed check.

    The requirements dict has to be defined as follows:
    Every entry in the dict maps from the field name to a 2-tuple (data_type, is_required),
    where `data_type` can be a python type like str, int, np.ndarray or ArrayWithShape to specify the
    data shape.
    The element `is_required` is an enum (see FieldRequired) which specifies if this field is optional.

    The requirements can be nested to represent groups. For this purpose, use a requirements
    dictionary as the `data_type` of one of the fields.

    Args:
        to_check: Nested dictionary to check against requirements
        requirements: As explained above
        base_name: String describing the location of `to_check` within the file (for better error messages only)
    """
    if isinstance(to_check, H5Group):
        available_datasets = {k for k in to_check if isinstance(to_check[k], H5Dataset)}
        available_groups = {k for k in to_check if isinstance(to_check[k], H5Group)}
    else:
        available_datasets = {k for k in to_check if not isinstance(to_check[k], dict)}
        available_groups = {k for k in to_check if isinstance(to_check[k], dict)}

    for field, requirement in requirements.items():
        is_group = isinstance(requirement[0], dict)

        if is_group:
            if field in available_groups:
                # Found a matching group (may or may not be optional)
                # Check recursively
                check_fields(to_check[field], requirement[0], base_name=f"{base_name}/{field}")
                available_groups.remove(field)
            else:
                if requirement[1] is FieldRequired.Required:
                    raise ValueError(f"Missing required group '{field}' in '{base_name}'")
        else:
            # This is a dataset not a group
            if field in available_datasets:
                if not check_dataset_type(to_check[field], requirement[0]):
                    raise ValueError(
                        f"Dataset '{field}' in '{base_name}' does not match required type '{requirement[0]}'"
                    )
                available_datasets.remove(field)
            else:
                if requirement[1] is FieldRequired.Required:
                    raise ValueError(f"Missing required dataset '{field}' in '{base_name}'")

    # Check if any available fields remain
    if len(available_groups) > 0:
        raise ValueError(f"Unknown groups {available_groups} in '{base_name}'")

    if len(available_datasets) > 0:
        raise ValueError(f"Unknown datasets {available_datasets} in '{base_name}'")


def check_listgroup_fields(listgroup: List[dict], requirements: Union[dict, Any], base_name: str = "") -> None:
    """Checks a list of instances against the requirements.
    The requirements apply to each item of the list, not to the list as a whole.
    Inside the HDF5 file, lists will be represented as groups containing multiple groups that
    have integers as names (but stored as string, because names have to be strings).
    In the native python dict format, we will use simple lists.
    """

    for item in listgroup:
        check_fields(item, requirements=requirements, base_name=base_name)


def h5_check_listgroup_fields(listgroup: H5Group, requirements: Union[dict, object], base_name: str = "") -> None:
    """Checks an H5Group that makes a list of instances against the requirements.
    The requirements apply to each item of the list, not to the list as a whole.
    Inside the HDF5 file, lists will be represented as groups containing multiple groups that
    have integers as names (but stored as string, because names have to be strings).
    """

    item_count = len(listgroup.keys())
    for idx in range(item_count):
        # We check if the group contains exactly the items named like "0", "1", ... "N"
        if str(idx) not in listgroup:
            raise ValueError(f"List group at {base_name} has {item_count} items but is missing index '{str(idx)}'")

        # Now check each item in the list if it's compliant with requirements
        check_fields(listgroup[str(idx)], requirements=requirements, base_name=base_name)


def check_dictgroup_fields(dictgroup: Dict[str, dict], requirements: Union[dict, object], base_name: str = "") -> None:
    """Checks a list-like dict of instances against the requirements.
    Almost like `check_listgroup_fields` but the elements are indexed by keys.
    The requirements apply to each item of the dict, not to the dict as a whole.
    """

    for item in dictgroup.values():
        check_fields(item, requirements=requirements, base_name=base_name)


def h5_check_dictgroup_fields(dictgroup: H5Group, requirements: Union[dict, object], base_name: str = "") -> None:
    """Checks an H5Group of similar sub-items against the requirements.
    Almost like `check_listgroup_fields` but the elements are indexed by keys.
    The requirements apply to each item of the group, not to the group as a whole.
    """

    for item in dictgroup.values():
        check_fields(item, requirements=requirements, base_name=base_name)


def check_file_meta_fields(file_meta: dict) -> None:
    check_fields(
        file_meta, requirements=format_requirements[GROUP_FILE_META][0], base_name=GROUP_FILE_META
    )  # type: ignore


def check_detection_fields(detections: list) -> None:
    check_listgroup_fields(
        detections,
        requirements=format_requirements[LISTGROUP_DETECTIONS][0],
        base_name=LISTGROUP_DETECTIONS,  # type: ignore
    )


def check_groundtruth_fields(groundtruth: dict) -> None:
    check_dictgroup_fields(
        groundtruth,
        requirements=format_requirements[DICTGROUP_GROUNDTRUTH][0],
        base_name=DICTGROUP_GROUNDTRUTH,  # type: ignore
    )


def check_volume_meta_fields(volume_meta: dict, volume: np.ndarray = None) -> None:
    check_fields(
        volume_meta, requirements=format_requirements[GROUP_VOLUME_META][0], base_name=GROUP_VOLUME_META
    )  # type: ignore

    # Check if meta data matches the volume, if we have one
    if volume is not None:
        if volume.shape != tuple(volume_meta[DSET_FULL_SHAPE]):
            raise ValueError("Volume shape does not match full shape given in meta data")


def h5_check_file_meta_fields(h5: H5File) -> None:
    try:
        file_meta_group = h5[GROUP_FILE_META]
    except KeyError:
        raise ValueError("Missing file_meta group")
    check_fields(
        file_meta_group, requirements=format_requirements[GROUP_FILE_META][0], base_name=GROUP_FILE_META
    )  # type: ignore


def h5_check_detection_fields(h5: H5File) -> None:
    try:
        detections_group = h5[LISTGROUP_DETECTIONS]
    except KeyError:
        raise ValueError("Missing detections group")
    h5_check_listgroup_fields(
        detections_group,
        requirements=format_requirements[LISTGROUP_DETECTIONS][0],
        base_name=LISTGROUP_DETECTIONS,  # type: ignore
    )


def h5_check_groundtruth_fields(h5: H5File) -> None:
    try:
        groundtruth_group = h5[DICTGROUP_GROUNDTRUTH]
    except KeyError:
        raise ValueError("Missing groundtruth group")
    h5_check_dictgroup_fields(
        groundtruth_group,
        requirements=format_requirements[DICTGROUP_GROUNDTRUTH][0],
        base_name=DICTGROUP_GROUNDTRUTH,  # type: ignore
    )


def h5_check_volume_meta_fields(h5: H5File) -> None:
    try:
        volume_meta_group = h5[GROUP_VOLUME_META]
    except KeyError:
        raise ValueError("Missing volume_meta group")

    check_fields(
        volume_meta_group, requirements=format_requirements[GROUP_VOLUME_META][0], base_name=GROUP_VOLUME_META
    )  # type: ignore

    # Check if meta data matches the volume, if we have one
    if DSET_VOLUME in h5:
        if not check_dataset_type(h5[DSET_VOLUME], format_requirements[DSET_VOLUME][0]):
            raise ValueError(
                f"Volume does not match required type '{format_requirements[DSET_VOLUME][0]}'. "
                f"Its type is {h5[DSET_VOLUME]}"
            )

        if tuple(h5[DSET_VOLUME].shape) != tuple(volume_meta_group[DSET_FULL_SHAPE]):
            raise ValueError("Volume shape does not match full shape given in meta data")


def h5_check_volcache(h5: H5File) -> None:
    """Checks the volume cache, which is usually optional. Here we require it"""

    try:
        volcache_group = h5[GROUP_VOLUME_META][GROUP_CACHE]
    except KeyError:
        raise ValueError("Missing volume cache group")

    check_fields(
        volcache_group,
        requirements=format_requirements[GROUP_VOLUME_META][0][GROUP_CACHE][0],  # type: ignore
        base_name=f"{GROUP_VOLUME_META}/{GROUP_CACHE}",
    )
