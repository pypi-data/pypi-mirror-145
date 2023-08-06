from os import path

from pydantic import BaseModel

from nwon_baseline.file_helper.file import file_extension_from_path


def save_pydantic_model_instance_as_json(
    pydantic_model: BaseModel, file_path: str
) -> str:
    """
    Saves the Pydantic Model instance as a json file.

    Expects the file_path to end with '.json'.
    If the suffix is not json we take the basename of the file_path and attach .json
    """

    suffix = file_extension_from_path(file_path)

    if suffix != ".json":
        splitted_file_name = path.basename(file_path).split(".")
        directory = path.dirname(file_path)

        if len(splitted_file_name) > 2:
            raise Exception(
                f"The file type of {path.basename(file_path)} needs to be json or it can't contain a dot."
            )
        elif len(splitted_file_name) == 2:
            file_path = path.join(directory, f"{splitted_file_name[0]}.json")

    with open(file_path, "w+", encoding="utf-8") as outfile:
        outfile.write(pydantic_model.json())

    return file_path
