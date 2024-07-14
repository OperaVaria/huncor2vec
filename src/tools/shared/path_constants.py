"""

path_constants.py

File path constants for the HunCor2Vec project.

"""

# Import.
from pathlib import Path

# Path constants:
PROJECT_DIR_PATH = Path(__file__).parents[3].resolve()
DOWNLOADS_DIR_PATH = PROJECT_DIR_PATH.joinpath("downloads/")
LINKS_DIR_PATH = PROJECT_DIR_PATH.joinpath("links/")
MODELS_DIR_PATH = PROJECT_DIR_PATH.joinpath("models/")
SRC_DIR_PATH = PROJECT_DIR_PATH.joinpath("src/")
TEMP_DIR_PATH = PROJECT_DIR_PATH.joinpath("tmp/")
CONFIG_FILE_PATH = SRC_DIR_PATH.joinpath("config.yml")
TEMP_TEXT_PATH = TEMP_DIR_PATH.joinpath("temp.txt")
TEMP_TSV_PATH = TEMP_DIR_PATH.joinpath("temp.tsv")
TEMP_GZ_PATH = TEMP_DIR_PATH.joinpath("temp.gz")

# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
