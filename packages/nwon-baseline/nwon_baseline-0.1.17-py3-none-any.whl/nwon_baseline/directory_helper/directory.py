import glob
import os
from typing import List


def file_names_in_directory(path: str):
    return [
        found_file
        for found_file in os.listdir(path)
        if os.path.isfile(os.path.join(path, found_file))
    ]


def directory_names_in_directory(path: str):
    return [
        found_file
        for found_file in os.listdir(path)
        if os.path.isdir(os.path.join(path, found_file))
    ]


def file_paths_in_directory(path: str) -> List[str]:
    return [
        os.path.join(path, found_file)
        for found_file in os.listdir(path)
        if os.path.isfile(os.path.join(path, found_file))
    ]


def file_paths_in_directory_with_extension(path: str, extension: str) -> List[str]:
    files_in_directory = file_paths_in_directory(path)
    return [file for file in files_in_directory if file.endswith(f".{extension}")]


def get_latest_file_in_directory(path: str):
    list_of_files = glob.glob(os.path.join(path, "*"))

    if len(list_of_files) > 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    return None


def clean_directory(path: str, recursive: bool = False):
    """
    Cleans all files in a directory. Optionally also deletes all sub
    directories including the containing files
    """

    for file_to_remove in file_names_in_directory(path):
        os.remove(os.path.join(path, file_to_remove))

    if recursive:
        for directory in directory_names_in_directory(path):
            clean_directory(directory, True)
            os.remove(directory)
