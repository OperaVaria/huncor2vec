"""

classes.py

Python classes of the HunCor2Vec project.

"""

# Imports:
import gzip
import logging
from os import scandir
from os.path import basename
from pathlib import Path
from shutil import copyfileobj
from typing import Iterator, List
from urllib.request import urlretrieve
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from gensim.test.utils import datapath
from gensim.utils import simple_preprocess
from pandas import read_csv
from .misc import dir_cleanup, load_config_file
from .path_constants import (
    CONFIG_FILE_PATH,
    TEMP_DIR_PATH,
    TEMP_GZ_PATH,
    TEMP_TEXT_PATH,
    TEMP_TSV_PATH,
)

# Load config file.
config_file = load_config_file(CONFIG_FILE_PATH)


class MyCorpus:
    """Represents a multi-file text corpus."""

    def __init__(self, source_type: str, source_path: Path) -> None:
        """Initialize object base attributes."""

        # Source file properties.
        self.source_type = source_type
        self.source_path = source_path

        # Temp file paths.
        self.temp_text_file = datapath(TEMP_TEXT_PATH)
        self.temp_tsv_file = datapath(TEMP_TSV_PATH)
        self.temp_gz_file = datapath(TEMP_GZ_PATH)

    def __iter__(self) -> Iterator[List[str]]:
        """Multi-file corpus iterator. Used to feed (yield) tokenized data
        line by line to the Word2Vec training method."""

        # If source is a list .txt of scraped URLs:
        if self.source_type == "list":
            yield from self._process_link_list()
        # If source is a directory with downloaded files.
        elif self.source_type == "dir":
            yield from self._process_directory()
        # Else: error.
        else:
            logging.error("Unknown source type: %s", self.source_type)

    def _process_link_list(self) -> Iterator[List[str]]:
        """Process a list of links to .gz files."""
        try:
            with open(self.source_path, mode="r", encoding="utf-8") as link_list:
                for link in link_list:
                    link = link.rstrip()  # Strip newline character.
                    self.download_gz(link, self.temp_gz_file)
                    self.file_type_handling(self.temp_gz_file)
                    yield from self._iterate_temp_text_file()
        except Exception as err_link_list:
            logging.exception("Error processing link list: %s", err_link_list)
            raise

    def _process_directory(self) -> Iterator[List[str]]:
        """Process a directory of .gz files."""
        try:
            for file in scandir(self.source_path):
                if file.name.lower().endswith(".gz"):
                    self.file_type_handling(file.path)
                    yield from self._iterate_temp_text_file()
        except Exception as err_files:
            logging.exception("Error processing directory: %s", err_files)
            raise

    def _iterate_temp_text_file(self) -> Iterator[List[str]]:
        """Iterate through the temporary text file and yield tokenized sentences."""
        try:
            with open(self.temp_text_file, mode="r", encoding="utf-8") as file:
                for line in file:
                    sentence = simple_preprocess(
                        line, min_len=config_file["Tokenizer"]["min-length"]
                    )
                    yield sentence
        except Exception as err_temp:
            logging.exception("Error while iterating temp text file: %s", err_temp)
            raise

    def file_type_handling(self, file: str) -> None:
        """Call appropriate functions based on corpus file type."""

        # Document is a preprepared .tsv with a "lemma" column.
        if ".tsv." in file:
            self.extract_gz(file, self.temp_tsv_file)
            self.convert_tsv(self.temp_tsv_file, self.temp_text_file)

        # File is a plain text file.
        else:
            self.extract_gz(file, self.temp_text_file)

    def download_gz(self, url: str, out_file: str) -> None:
        """Download a .gz file."""
        filename = basename(url)
        logging.info("Downloading %s", filename)
        try:
            urlretrieve(url, out_file)
        except Exception as err_download:
            logging.exception("Error downloading %s: %s", url, err_download)
            raise

    def extract_gz(self, gz_file: str, out_file: str) -> None:
        """Extract and save the content of a .gz file."""
        filename = basename(gz_file)
        logging.info("Uncompressing %s", filename)
        try:
            with gzip.open(gz_file, "r") as f_in, open(out_file, "wb") as f_out:
                copyfileobj(f_in, f_out)
        except Exception as err_extract:
            logging.exception("Error extracting %s: %s", gz_file, err_extract)
            raise

    def convert_tsv(self, tsv_file: str, out_file: str) -> None:
        """Create a .txt file with continuous text from the .tsv lemma column.
        One line = one sentence."""
        try:
            # Read .tsv file's lemma column to a pandas DataFrame.
            df = read_csv(
                tsv_file,
                engine="c",
                on_bad_lines="warn",
                sep="\t",
                quoting=3,
                usecols=["lemma"],
            )
            # Remove NaN rows.
            df.dropna(how="all", inplace=True)
            # Convert to Python list.
            df_list = list(df["lemma"])
            # Write words to out_file (min_length 3), add newline in place of sentence
            # closing punctuations.
            with open(out_file, mode="w+", encoding="utf-8") as f:
                for word in df_list:
                    if len(word) > 2:
                        f.write(f"{word} ")
                    elif word in [".", ";", "?", "!"]:
                        f.write("\n")
        except Exception as err_tsv:
            logging.exception("Error converting TSV %s: %s", tsv_file, err_tsv)
            raise


class AutoSaver(CallbackAny2Vec):
    """Callback class to save the trained model after each epoch and
    at the end of all training operations."""

    def __init__(self, model_path: Path) -> None:
        """Initialize object with base attributes."""
        self.model_path = model_path
        self.model_file_name = basename(model_path)
        self.epoch = 0

    def on_epoch_end(self, model: Word2Vec) -> None:
        """Called at the end of each epoch.
        Autosave temporary model files."""
        file_name = f"AUTOSAVE_epoch{self.epoch}_{self.model_file_name}"
        output_path = datapath(TEMP_DIR_PATH.joinpath(file_name))
        model.save(output_path)
        logging.info("Autosaved model at end of epoch %d.", self.epoch)
        self.epoch += 1

    def on_train_end(self, model: Word2Vec) -> None:
        """Called at the end of all training operations. Saves
        model and removes temporary files."""
        model.save(self.model_path)
        logging.info("Removing temporary files.")
        dir_cleanup(TEMP_DIR_PATH, (".gz", ".mdl", ".npy", ".tsv", ".txt"))
