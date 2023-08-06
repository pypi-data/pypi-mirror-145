# -*- coding: utf-8 -*-
"""
    This module provides functions to verify uval HDF5 files.
    It reports any problems that a set of existing HDF5 may have.
    Any missing required field in HDF5 file will be reported as a problem
"""

from pathlib import Path
from typing import Dict, List

from uval.utils.hdf5_format import (
    DSET_VOLUME,
    h5_check_detection_fields,
    h5_check_file_meta_fields,
    h5_check_groundtruth_fields,
    h5_check_volcache,
    h5_check_volume_meta_fields,
)
from uval.utils.hdf5_io import UvalHdfFileInput


def verify_single_hdf5_file(file_path: str) -> list:
    """
        Checks a single hdf5 file and returns a list of error descriptions.
    Args:
        file_path: The HDF5 file path to be verified

    Returns:
        A list of problems detected in HDF5 file
    """
    problems = []

    # Check file name (extensions)
    lowercase_extensions = [s.lower() for s in Path(file_path).suffixes]
    extension_ok = False

    if lowercase_extensions[-1] == ".h5" and len(lowercase_extensions) >= 2:
        # Now check second level extension (second to last)
        if lowercase_extensions[-2] in [".det", ".gt", ".voldata", ".volcache"]:
            extension_ok = True

    if not extension_ok:
        return [
            "File must have a valid extension (one of '.det.h5', '.gt.h5', '.voldata.h5', '.volcache.h5'). "
            "Won't check its contents."
        ]

    with UvalHdfFileInput(file_path) as f:
        try:
            # Check file_meta
            h5_check_file_meta_fields(f.h5)
        except ValueError as e:
            problems += [str(e)]

        try:
            # Check volume_meta
            h5_check_volume_meta_fields(f.h5)
        except ValueError as e:
            problems += [str(e)]

        try:
            # Check contents depending on file name
            if lowercase_extensions[-2] == ".det":
                h5_check_detection_fields(f.h5)
            elif lowercase_extensions[-2] == ".gt":
                h5_check_groundtruth_fields(f.h5)
            elif lowercase_extensions[-2] == ".voldata":
                # Voldata is automatically checked in h5_check_volume_meta_fields above if available
                # Here we just check it's available at all
                if DSET_VOLUME not in f.h5:
                    raise ValueError("File does not contain volume data")
            elif lowercase_extensions[-2] == ".volcache":
                h5_check_volcache(f.h5)
        except ValueError as e:
            problems += [str(e)]

    return problems


def verify_hdf5_files(
    folder_path: str, recursive: bool = False, file_filter: str = "*.h5", print_problems: bool = True
) -> Dict[str, List[str]]:
    """
        Give a folder, finds and verifies all HDF5 files inside. This can be recursive or filtered if desired.
    Returns a dictionary with all the problems found for each file.
    Args:
        folder_path: The path to folder containing HDF5 files
        recursive: To parse the folder recursively or not
        file_filter: The wildcard to include HDF5 files by name
        print_problems: To print the detected problems in standard output or not

    Returns:
        A dictionary containing all the detected problems including the file name and problem description
    """

    # A dictionary mapping from file path to a list of strings with problem descriptions
    all_problems = {}

    # Find all HDF5 files that could be relevant
    if recursive:
        filepath_generator = Path(folder_path).glob(f"**/{file_filter}")
    else:
        filepath_generator = Path(folder_path).glob(file_filter)

    for file_path in filepath_generator:
        file_path_str = str(file_path.resolve())
        problems = verify_single_hdf5_file(file_path_str)
        if len(problems):
            all_problems[file_path_str] = problems

    if print_problems:
        for filepath in sorted(all_problems.keys()):
            print(f"\n{filepath}:")
            for p in all_problems[filepath]:
                print(f"- {p}")

    return all_problems
