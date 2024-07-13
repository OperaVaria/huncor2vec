"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
import logging
from os import scandir
from os.path import isfile
from pick import pick
from yaml import safe_load


def check_dirs(dirs):
    """Check if required directories exist,
    if not, create them."""
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def file_select_loop(prompt, dir_path):
    """Prompt loop to select an existing file inside
    a given directory."""
    while True:
        file_name = input(prompt)
        file_path = dir_path.joinpath(file_name)
        if isfile(file_path):
            break
        print("File does not exist!")
    return file_path


def file_select_menu(prompt, dir_path, file_ext):
    """Create a pick menu to select a file from a given directory.
    Filters based on file extension. Returns selected file path."""
    title = prompt
    options = [
        file.name for file in scandir(dir_path) if file.name.lower().endswith(file_ext)
    ]

    # If no files with the proper file ext present: error.
    if not options:
        logging.warning("No files found!")
        raise FileNotFoundError(
            f"No files with extension {file_ext} found in {dir_path}"
        )

    option, _ = pick(options, title, indicator="=>", default_index=0)
    selected_file = dir_path.joinpath(option)
    return selected_file


def load_config_file(file_path):
    """Safely load a YAML config file with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as conf_file_cont:
            config_file = safe_load(conf_file_cont)
    except FileNotFoundError:
        logging.error("config file not found at: %s", file_path)
        raise
    except Exception as e_config:
        logging.error("error reading config file: %s", e_config)
        raise
    return config_file


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
