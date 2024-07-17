"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
import logging
from os import remove, scandir
from os.path import isfile
from pathlib import Path
from sys import exit as sys_exit
from typing import List, Tuple
from pick import pick
from yaml import safe_load


def yes_no_menu(prompt_text: str) -> bool:
    """Pick menu to confirm a choice. Returns the
    confirmation value."""

    # Menu variables.
    title = prompt_text
    options = ["1. Yes", "2. No", "3. Cancel"]
    _, index = pick(options, title, indicator="=>", default_index=0)

    # Menu switch.
    match index:
        case 0:  # Yes
            confirm = True
        case 1:  # No
            confirm = False
        case 2:  # Cancel (exit script)
            sys_exit(0)
        case _:  # Incorrect selection (should not happen).
            error_crash("Selection error!")

    return confirm


def file_select_loop(prompt_text: str, dir_path: Path) -> Path:
    """Prompt loop to select an existing file inside
    a given directory."""
    while True:
        file_name = input(prompt_text)
        file_path = dir_path.joinpath(file_name)
        if isfile(file_path):
            break
        print("File does not exist!")
    return file_path


def file_select_menu(prompt_text: str, dir_path: Path, file_ext: str) -> None | Path:
    """Create a pick menu to select a file from a given directory.
    Filters based on file extension. Returns selected file path."""

    # Set title and options.
    title = prompt_text
    options = [
        file.name for file in scandir(dir_path) if file.name.lower().endswith(file_ext)
    ]

    # If no files with the proper file extension present:
    # notify and set return value to None.
    if not options:
        logging.error("No files found in %s", dir_path)
        selected_file = None
        input("Press Enter to continue...")
    else:
        option, _ = pick(options, title, indicator="=>", default_index=0)
        selected_file = dir_path.joinpath(option)

    return selected_file


def check_dirs(dirs: List[Path]) -> None:
    """Check if required directories exist,
    if not, create them."""
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def dir_cleanup(dir_path: Path, file_ext: str | Tuple[str]) -> None:
    """Remove all files from a directory with a certain
    file extension"""

    # File removal loop with error handling.
    for file in scandir(dir_path):
        if file.name.lower().endswith(file_ext):
            try:
                remove(file.path)
                logging.info("%s removed.", file.path)
            except (FileNotFoundError, OSError) as err_remove:
                logging.error("Error removing file %s: %s", file.path, err_remove)

    # Operation end prompt.
    logging.info("Process completed.")
    input("Press Enter to continue...")


def load_config_file(file_path: Path) -> dict:
    """Safely load a YAML config file with error handling.
    Returns the full config file hierarchy."""
    try:
        with open(file_path, "r", encoding="utf-8") as conf_file_cont:
            config_dict = safe_load(conf_file_cont)
    except FileNotFoundError:
        logging.error("Config file not found at %s", file_path)
        raise
    except Exception as err_config:
        logging.exception("Error reading config file: %s", err_config)
        raise
    return config_dict


def default_logging() -> None:
    """Set default logging settings."""
    logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
    )


def error_crash(message: str) -> None:
    """Function to handle serious errors.
    Logs critical error message and exits program.
    Exit status 1."""
    logging.critical(message)
    sys_exit(1)


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
