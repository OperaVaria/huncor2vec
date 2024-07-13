"""

classes.py

Python classes of the HunCor2Vec project.

"""

# Imports:
import gzip
import logging
from os import scandir, remove
from os.path import basename
from shutil import copyfileobj
from urllib.request import urlretrieve
from gensim import utils
from gensim.models.callbacks import CallbackAny2Vec
from gensim.test.utils import datapath
from pandas import read_csv
from .misc import load_config_file
from .path_constants import (
    CONFIG_FILE_PATH,
    TEMP_DIR_PATH,
    TEMP_GZ_PATH,
    TEMP_TEXT_PATH,
    TEMP_TSV_PATH,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

# Load config file.
config_file = load_config_file(CONFIG_FILE_PATH)


class MyCorpus:
    """Represents a multi-file text corpus."""

    def __init__(self, source_type, source_path):
        """Initialize object base attributes."""

        # Source file properties.
        self.source_type = source_type
        self.source_path = source_path

        # Temp file paths.
        self.temp_text_file = datapath(TEMP_TEXT_PATH)
        self.temp_tsv_file = datapath(TEMP_TSV_PATH)
        self.temp_gz_file = datapath(TEMP_GZ_PATH)

    def __iter__(self):
        """Multi-file corpus iterator. Used to feed tokenized data
        line by line to the Word2Vec training method."""

        # If source is a list .txt of scraped urls:
        if self.source_type == "list":
            yield from self._process_link_list()
        # If source is a directory with downloaded files.
        elif self.source_type == "dir":
            yield from self._process_directory()
        # Else: error.
        else:
            logging.error("unknown source type: %s", self.source_type)

    def _process_link_list(self):
        """Process a list of links to .gz files."""
        try:
            with open(self.source_path, mode="r", encoding="utf-8") as link_list:
                for link in link_list:
                    link = link.rstrip()  # Strip newline character.
                    self.download_gz(link, self.temp_gz_file)
                    self.file_type_handling(self.temp_gz_file)
                    yield from self._iterate_temp_text_file()
        except Exception as e_link_list:
            logging.error("error processing link list: %s", e_link_list)
            raise

    def _process_directory(self):
        """Process a directory of .gz files."""
        try:
            for file in scandir(self.source_path):
                if file.name.lower().endswith(".gz"):
                    self.file_type_handling(file.path)
                    yield from self._iterate_temp_text_file()
        except Exception as e_files:
            logging.error("error processing files: %s", e_files)
            raise

    def _iterate_temp_text_file(self):
        """Iterate through the temporary text file and yield tokenized sentences."""
        try:
            with open(self.temp_text_file, mode="r", encoding="utf-8") as file:
                for line in file:
                    sentence = utils.simple_preprocess(
                        line, min_len=config_file["Tokenizer"]["min-length"]
                    )
                    yield sentence
        except Exception as e_temp:
            logging.error("error iterating temp text file: %s", e_temp)
            raise

    def file_type_handling(self, file):
        """Call appropriate functions based on corpus file type."""

        # Document is a preprepared .tsv with a "lemma" column.
        if ".tsv." in file:
            self.extract_gz(file, self.temp_tsv_file)
            self.convert_tsv(self.temp_tsv_file, self.temp_text_file)

        # File is a plain text file.
        else:
            self.extract_gz(file, self.temp_text_file)

    def download_gz(self, url, out_file):
        """Download a .gz file."""
        filename = basename(url)
        logging.info("downloading %s", filename)
        try:
            urlretrieve(url, out_file)
        except Exception as e_download:
            logging.error("error downloading %s: %s", url, e_download)
            raise

    def extract_gz(self, gz_file, out_file):
        """Extract and save the content of a .gz file."""
        filename = basename(gz_file)
        logging.info("uncompressing %s", filename)
        try:
            with gzip.open(gz_file, "r") as f_in, open(out_file, "wb") as f_out:
                copyfileobj(f_in, f_out)
        except Exception as e_extract:
            logging.error("error extracting %s: %s", gz_file, e_extract)
            raise

    def convert_tsv(self, tsv_file, out_file):
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
        except Exception as e_tsv:
            logging.error("error converting TSV %s: %s", tsv_file, e_tsv)
            raise


class AutoSaver(CallbackAny2Vec):
    """Callback class to save the trained model after each epoch and
    at the end of all training operations."""

    def __init__(self, model_path):
        """Initialize object with base attributes."""
        self.model_path = model_path
        self.model_file_name = basename(model_path)
        self.epoch = 0

    def on_epoch_end(self, model):
        """Called at the end of each epoch.
        Autosave temporary model files."""
        file_name = f"AUTOSAVE_epoch{self.epoch}_{self.model_file_name}"
        output_path = datapath((TEMP_DIR_PATH).joinpath(file_name))
        model.save(output_path)
        logging.info("autosaved model at end of epoch %d.", self.epoch)
        self.epoch += 1

    def on_train_end(self, model):
        """Called at the end of all training operations. Saves
        model and removes temporary files."""
        model.save(self.model_path)
        for file in scandir(TEMP_DIR_PATH):
            if file.name.lower().endswith((".gz", ".mdl", ".npy", ".tsv", ".txt")):
                try:
                    remove(file.path)
                    logging.info("removed temporary file: %s", file.path)
                except (FileNotFoundError, OSError) as e_remove:
                    logging.error("error removing file %s: %s", file.path, e_remove)
