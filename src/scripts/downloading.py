"""

downloading.py

Script to download all files from a previously scraped list of
corpus files.

Part of the HunCor2Vec project.

"""

# Imports:
from os.path import basename
from urllib.request import urlretrieve

# Conditional imports (to be runnable as a stand-alone script).
if __name__ == "__main__":
    from shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from shared.misc import file_select_menu
else:
    from scripts.shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from scripts.shared.misc import file_select_menu


def download_all(list_file, out_folder):
    """Download all files from the urls listed in the link list file."""
    with open(list_file, mode="r", encoding="utf-8") as link_list:
        for line_index, link in enumerate(link_list):
            # Strip newline.
            link = link.rstrip()
            # Set variables
            file_name = basename(link)
            if file_name == "":
                file_name = "unknown.unk"
            out_file_path = (out_folder).joinpath(file_name)
            # Retrieve with error handling:
            print(f"Downloading {file_name}...")
            try:
                urlretrieve(link, out_file_path)
            except ValueError:
                print(f"Unknown URL type on line {line_index}!")
                print("Failed.")
            else:
                print("Completed.")


def main():
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
