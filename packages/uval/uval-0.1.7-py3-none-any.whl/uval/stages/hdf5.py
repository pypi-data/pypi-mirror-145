# -*- coding: utf-8 -*-
"""This module include stages that are used to find and load HDF5 files from disk.
The result will be returned as a Hdf5FilesData object
"""

import warnings  # type: ignore
from concurrent.futures import ThreadPoolExecutor, as_completed  # type: ignore
from glob import glob  # type: ignore
from os import path, stat  # type: ignore
from typing import Tuple  # type: ignore

from rich.progress import Progress

from uval.context import get_context  # type: ignore
from uval.stages.stage import uval_stage  # type: ignore
from uval.stages.stage_data import DatasetSpecificationData, Hdf5FilesData  # type: ignore
from uval.utils.hdf5_io import UvalHdfFileInput  # type: ignore
from uval.utils.log import logger  # type: ignore


def _read_single_file_meta(file_path: str):
    with UvalHdfFileInput(file_path) as f:
        return file_path, {
            "file_meta": f.file_meta(),
            "volume_meta": f.volume_meta(),
            "detections": f.detections(include_masks=False, include_caches=False),
            "groundtruth": f.ground_truth(include_masks=False, include_caches=False),
        }


def load_hdf5_files(
    folder_path: str,
    recursive: bool = False,
    file_filter: str = "*.h5",
    list_of_files=None,
    ignore_missing_files=False,
    max_workers=None,
) -> Hdf5FilesData:
    """This function searches for uval compatible HDF5 files in the given folder.
    It will load their meta data to make sure we can match and access them quickly by volume id."""

    config = get_context(max_workers=max_workers).config["hdf5_io"]

    # Set up result data store
    stage_results = Hdf5FilesData()

    # Find all HDF5 files that could be relevant
    if list_of_files is None or recursive:
        if recursive:
            file_list = glob(path.join(folder_path, "**", file_filter), recursive=True)
        else:
            file_list = glob(path.join(folder_path, file_filter), recursive=False)
    else:
        file_list = list_of_files
    logger.debug("file_list")

    all_futures = set()
    with ThreadPoolExecutor(max_workers=config["num_threads"]) as executor:

        # Submit all jobs to the pool
        for file_name in file_list:
            all_futures.add(executor.submit(_read_single_file_meta, file_name))
        """
        for file_name in file_list:
            if path.exists(file_name):
                all_futures.add(executor.submit(_read_single_file_meta, file_name))
            elif ignore_missing_files:
                logger.warning(f"HDF5 file does not exist: '{file_name}'")
            else:
                raise IOError(f"HDF5 file does not exist: '{file_name}'")
        """
        # Wait for each to complete
        for future in as_completed(all_futures):
            file_path, meta = future.result()

            # Store meta data into results StageData in a way that it is easily accessible by its bag_id
            try:
                volume_id = meta["volume_meta"]["id"]
                stage_results.table.loc[volume_id] = {
                    "volume_id": volume_id,
                    "file_path": file_path,
                    "file_stat": stat(file_path),  # We need this to check if the file changed
                    "hdf5_meta": meta,
                }
            except KeyError as e:

                # We found an invalid HDF5 file, log this
                logger.warning(f"HDF5 file is missing some fields: '{file_path}'")
                raise (e)

    return stage_results


@uval_stage
def load_gt(
    folder_path: str, recursive: bool = False, dataset=None, ignore_missing_files=False, max_workers=None
) -> Hdf5FilesData:
    """Ground truth in non negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        Hdf5FilesData: Ground truths in positive images.
    """
    if dataset is None:
        warnings.warn("Old usage!")
    list_of_files = []
    if dataset is not None:
        list_of_files = dataset.table[~dataset.table.is_negative]["volume_id"].tolist()

    file_list_full = [path.join(folder_path, file + ".gt.h5") for file in list_of_files]
    try:
        gt_files = load_hdf5_files(
            folder_path,
            recursive,
            file_filter="*.gt.h5",
            list_of_files=file_list_full,
            ignore_missing_files=ignore_missing_files,
            max_workers=max_workers,
        )
    except FileNotFoundError as e:
        raise Exception("Ground Truth files and YAML mismatch.") from e
    return gt_files


@uval_stage
def load_detections(
    folder_path: str, recursive: bool = False, dataset=None, ignore_missing_files=False, max_workers=None
) -> Hdf5FilesData:
    """Detections in non negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        Hdf5FilesData: Detections in positive images.
    """
    if dataset is None:
        warnings.warn("Old usage!")
    list_of_files = []

    if dataset is not None:
        list_of_files = dataset.table[~dataset.table.is_negative]["volume_id"].tolist()
    file_list_full = [path.join(folder_path, file + ".det.h5") for file in list_of_files]
    try:
        files_det = load_hdf5_files(
            folder_path,
            recursive,
            file_filter="*.det.h5",
            list_of_files=file_list_full,
            ignore_missing_files=ignore_missing_files,
            max_workers=max_workers,
        )
    except FileNotFoundError as e:
        raise Exception("Detection files and YAML mismatch.") from e
    return files_det


@uval_stage
def load_negatives(
    folder_path: str,
    recursive: bool = False,
    dataset: DatasetSpecificationData = None,
    ignore_missing_files: bool = False,
    max_workers=None,
) -> Hdf5FilesData:
    """Detections in negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        Hdf5FilesData: Detections in Negative images.
    """
    list_of_files = []
    if dataset is not None:
        list_of_files = dataset.table[dataset.table.is_negative]["volume_id"].tolist()
    file_list_full = [path.join(folder_path, file + ".det.h5") for file in list_of_files]

    try:
        files_soc = load_hdf5_files(
            folder_path,
            recursive,
            file_filter="*.det.h5",
            list_of_files=file_list_full,
            ignore_missing_files=ignore_missing_files,
            max_workers=max_workers,
        )
    except FileNotFoundError as e:
        raise Exception("Negative detection files and YAML mismatch.") from e
    return files_soc


@uval_stage
def load_evaulation_files(
    folder_path: str, recursive=False, dataset=None, ignore_missing_files=False, max_workers=None
) -> Tuple[Hdf5FilesData, Hdf5FilesData, Hdf5FilesData]:
    """This is a wrapper that calls underlying functions and loads positive
    detections, GTs and negative detections.

    Args:
        folder_path (str): path to the data folder.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The input dataset
        loaded from YAML file. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Returns:
        Hdf5FilesData: Tuple including all three parts of the dataset.
    """
    neg = set(dataset.table[dataset.table.is_negative]["volume_id"].tolist())
    pos = set(dataset.table[~dataset.table.is_negative]["volume_id"].tolist())
    if len(neg & pos) > 0:
        raise ValueError("The positive and negative subsets have overlap.")

    with Progress() as progress:
        task = progress.add_task("[red]Loading...", total=3)
        detections: Hdf5FilesData = load_detections(
            path.join(folder_path, "detections"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        )
        progress.update(task, advance=1)
        groundtruths: Hdf5FilesData = load_gt(
            path.join(folder_path, "raw"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        )
        progress.update(task, advance=1)
        negatives: Hdf5FilesData = load_negatives(
            path.join(folder_path, "detections"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        )
        progress.update(task, advance=1)
    return detections, groundtruths, negatives
