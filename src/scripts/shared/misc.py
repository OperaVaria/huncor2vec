"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
import logging
from os import scandir
from os.path import isfile
from pathlib import Path
from typing import List
from pick import pick
from yaml import safe_load


def check_dirs(dirs: List[Path]) -> None:
    """Check if required directories exist,
    if not, create them."""
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def file_select_loop(prompt: str, dir_path: Path) -> Path:
    """Prompt loop to select an existing file inside
    a given directory."""
    while True:
        file_name = input(prompt)
        file_path = dir_path.joinpath(file_name)
        if isfile(file_path):
            break
        print("File does not exist!")
    return file_path


def file_select_menu(prompt: str, dir_path: Path, file_ext: str) -> Path:
    """Create a pick menu to select a file from a given directory.
    Filters based on file extension. Returns selected file path."""
    title = prompt
    options = [
        file.name for file in scandir(dir_path) if file.name.lower().endswith(file_ext)
    ]

    # If no files with the proper file ext present: error.
    if not options:
        raise FileNotFoundError(
            f"No files with extension {file_ext} found in {dir_path}"
        )

    option, _ = pick(options, title, indicator="=>", default_index=0)
    selected_file = dir_path.joinpath(option)
    return selected_file


def load_config_file(file_path: Path) -> dict:
    """Safely load a YAML config file with error handling.
       Returns a dict of the config file hierarchy."""
    try:
        with open(file_path, "r", encoding="utf-8") as conf_file_cont:
            config_dict = safe_load(conf_file_cont)
    except FileNotFoundError:
        logging.error("config file not found at: %s", file_path)
        raise
    except Exception as e_config:
        logging.error("error reading config file: %s", e_config)
        raise
    return config_dict


# Print on accidental run:
if __name__ == "__main__":
    config_file_test = load_config_file("D:\\Programozás\\Python\\huncor2vec\\src\\config.yml")
    print (config_file_test)
    
