"""This module provides simple functions to read and write YAML files.
The data structure for pure YAML IO operations would be the dictionary
"""

from os import W_OK, access, path
from typing import Dict

from ruamel.yaml import YAML

from uval.utils.log import logger


def load_yaml_data(yaml_file_path: str) -> Dict:
    """
        loads data from a YAML file into a directory structure and returns dict type
        If the file does not exist or not read properly, returns None.
    Args:
        yaml_file_path: The path to the YAML file

    Returns:
        Data read from YAML file in dictionary format
    """
    if not path.exists(yaml_file_path):
        logger.critical("The YAML file '{}' does not exist!")
        return dict()
    try:
        yaml = YAML()
        with open(yaml_file_path, "r") as f:
            data_dict = yaml.load(f)
        return data_dict
    except Exception as e:
        logger.error("Could read YAML data from the file '{}': {}".format(yaml_file_path, e.__str__()))
        return dict()


def store_yaml_data(data_dict: dict, yaml_file_path: str) -> bool:
    """
        Stores a dictionary type data into YAML file and returns True
        If the folder is not writable of there's a problem with the writing, it returns False

    Args:
        data_dict:
        yaml_file_path:

    Returns:
        Returns true if YAML stored successfully, otherwise returns false
    """
    writing_dir = path.dirname(path.abspath(yaml_file_path))
    if not access(writing_dir, W_OK):
        logger.error("Unable to write into the destination folder '{}'!".format(writing_dir))
        return False

    yaml = YAML()
    try:
        with open(yaml_file_path, "w") as f:
            yaml.dump(data_dict, f)
        return True
    except Exception as e:
        logger.error("Could not write YAML data into the file '{}': {}".format(yaml_file_path, e.__str__()))
        return False
