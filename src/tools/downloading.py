"""

downloading.py

Script to download all files from a previously scraped list of
corpus files.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from pathlib import Path
from os.path import basename
from urllib.error import URLError
from urllib.request import urlretrieve
from pick import pick

# Conditional imports (to be runnable as a stand-alone script):
if __name__ == "__main__":
    from shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from shared.misc import (
        check_dirs,
        dir_cleanup,
        error_crash,
        default_logging,
        file_select_menu,
        yes_no_menu,
    )
else:
    from tools.shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from tools.shared.misc import (
        check_dirs,
        dir_cleanup,
        error_crash,
        default_logging,
        file_select_menu,
        yes_no_menu,
    )

def download_menu() -> None:
    """Download task select menu: download corpus files from link list
       or cleanup previous downloads."""

    # Menu variables.
    title = "Webcorpus 2.0 Downloader\nSelect a task: "
    options = ["1. Download packages", "2. Package cleanup", "3. Exit"]

    # Menu loop.
    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:  # Download corpus files from url list.
                # Select list file.
                list_path = file_select_menu(
                    "Webcorpus 2.0 Downloader\nSelect a list file: ", LINKS_DIR_PATH, ".txt"
                )
                # If a legitimate file selected, call download_all function:
                if list_path:
                    download_all(list_path, DOWNLOADS_DIR_PATH)
            case 1:  # Cleanup with confirmation.
                confirm = yes_no_menu("Delete all files in the downloads folder?")
                # Positive confirmation: delete all .gz files from downloads/ dir.
                if confirm:
                    dir_cleanup(DOWNLOADS_DIR_PATH, (".gz", ".mdl", ".npy", ".tsv", ".txt"))
            case 2: # Exit (break loop).
                break
            case _:  # Incorrect selection (should not happen).
                error_crash("Selection error!")


def download_all(list_file: Path, out_folder: Path) -> None:
    """Download all files from the URLs listed in the link list file."""

    # File downloading loop.
    with open(list_file, mode="r", encoding="utf-8") as link_list:
        for line_index, link in enumerate(link_list):
            # Strip newline.
            link = link.rstrip()
            # Set variables
            file_name = basename(link)
            if not file_name:
                file_name = f"unknown_{line_index}.unk"
            out_file_path = out_folder.joinpath(file_name)
            # Retrieve with error handling:
            logging.info("Downloading %s...", file_name)
            try:
                urlretrieve(link, out_file_path)
            except ValueError as err_unk_type:
                logging.error("Download failed! Error on line %d: %s", line_index, err_unk_type)
            except URLError as err_url:
                logging.error("Error downloading %s: %s", file_name, err_url)
            else:
                logging.info("Completed.")

    # Operation end prompt.
    logging.info("Files have been downloaded to %s", DOWNLOADS_DIR_PATH)
    input("Press Enter to return...")


def main() -> None:
    """Main function."""
    logging.info("Launching the Webcorpus 2.0 Downloader tool.")
    # Launch task select menu:
    download_menu()


# Run when launched as standalone script.
if __name__ == "__main__":
    # Set default logging settings.
    default_logging()
    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH, DOWNLOADS_DIR_PATH])
    # Launch main function.
    main()
    # Ending message.
    logging.info("Exiting...")
