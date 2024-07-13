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

# Conditional imports (to be runnable as a stand-alone script):
if __name__ == "__main__":
    from shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from shared.misc import file_select_menu
else:
    from scripts.shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from scripts.shared.misc import file_select_menu

# Configure logging
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

def download_all(list_file: Path, out_folder: Path) -> None:
    """Download all files from the URLs listed in the link list file."""
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
            logging.info("downloading %s...", file_name)
            try:
                urlretrieve(link, out_file_path)
            except ValueError as e_unknown_type:
                logging.error("unknown URL type on line %d: %s", line_index, e_unknown_type)
                logging.info("failed.")
            except URLError as e_url:
                logging.error("error downloading %s: %s", file_name, e_url)
                logging.info("failed.")
            else:
                logging.info("completed.")

def main() -> None:
    """Main function."""

    print("\nHunCor2 Downloader\n")

    # Get input (filename).
    list_path = file_select_menu(
        "HunCor2 Downloader\nSelect list file: ", LINKS_DIR_PATH, ".txt"
    )

    # If does not exist, create downloads/ dir.
    DOWNLOADS_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # Call download function.
    download_all(list_path, DOWNLOADS_DIR_PATH)

    # End prompt.
    print(f"The files have been downloaded to:\n{DOWNLOADS_DIR_PATH}")
    input("\nPress Enter to continue...")


# Run when launched as standalone script.
if __name__ == "__main__":
    main()
    print("Exiting...")
