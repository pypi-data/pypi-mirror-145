import glob
import os
import shutil
from os import path
from pathlib import Path
from typing import List

from nwon_baseline.file_helper.file import file_extension_from_path


def create_pathes(pathes: List[str]) -> None:
    for path_to_create in pathes:
        Path(path_to_create).mkdir(parents=True, exist_ok=True)


def copy_directory(source_directory: str, target_directory: str) -> None:
    if path.exists(target_directory):
        shutil.rmtree(target_directory)

    shutil.copytree(source_directory, target_directory)


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


def file_paths_in_directory_with_extension(
    path: str, file_extensions: List[str]
) -> List[str]:
    """
    Returns a list of files in a directory that has the defined extension.
    File extensions can be defined with or without a dot in the beginning.
    """

    extensions = [
        extension if extension.startswith(".") else f".{extension}"
        for extension in file_extensions
    ]

    files_in_directory = file_paths_in_directory(path)
    return [
        file
        for file in files_in_directory
        if file_extension_from_path(file) in extensions
    ]


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
