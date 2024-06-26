""" 

downloading.py

Script to download all files from a previously scraped list of
corpus files.

Part of the HunCor2Vec project.

"""

# Imports.
from os.path import basename
from urllib.request import urlretrieve

# Conditional imports (to be runnable as a stand-alone script).
if __name__ == '__main__':
    from shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from shared.misc import file_select_menu
else:
    from scripts.shared.path_constants import LINKS_DIR_PATH, DOWNLOADS_DIR_PATH
    from scripts.shared.misc import file_select_menu


def download_all(list_file, out_folder):
    """ Download all files from the urls listed in the link list file. """
    with open(list_file, mode="r", encoding="utf-8") as link_list:
        for link in link_list:
            link = link.rstrip() # Strip newline.
            file_name = basename(link)
            out_file_path = (out_folder).joinpath(file_name)
            print(f"Downloading {file_name}...")
            urlretrieve(link, out_file_path)
            print("Completed.")


def main():
    """ Main function. """

    # Get input (filename).
    list_path = file_select_menu("HunCor2 Downloader\n\nSelect list file: ", LINKS_DIR_PATH, ".txt")

    # If does not exist, create downloads/ dir.
    DOWNLOADS_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # Call download function.
    download_all(list_path, DOWNLOADS_DIR_PATH)

    # End prompt.
    print(f"All files have been downloaded to:\n{DOWNLOADS_DIR_PATH}")
    input("\nPress Enter to continue...")


# Run when launched as standalone script.
if __name__ == '__main__':
    main()
    print("Exiting...")
