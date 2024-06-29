"""

classes.py

Python classes of the for the HunCor2Vec project.

"""

# Imports:
import gzip
from os import scandir
from os.path import basename
from shutil import copyfileobj
from urllib.request import urlretrieve
from gensim import utils
from gensim.models.callbacks import CallbackAny2Vec
from gensim.test.utils import datapath
from pandas import read_csv
from yaml import safe_load
from .path_constants import CONFIG_FILE_PATH, TEMP_GZ_PATH, TEMP_TEXT_PATH, TEMP_TSV_PATH

# Load config file.
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as conf_file_cont:
    config_file = safe_load(conf_file_cont)


class MyCorpus:
    """Represents a multi-file text corpus."""

    def __init__(self, source_type, source_path):
        """Object base attributes."""

        # Source file properties.
        self.source_type = source_type
        self.source_path = source_path

        # Temp file paths.
        self.temp_text_file = datapath(TEMP_TEXT_PATH)
        self.temp_tsv_file = datapath(TEMP_TSV_PATH)
        self.temp_gz_file = datapath(TEMP_GZ_PATH)

    def __iter__(self):
        """Multi-file corpus iterator. Used to feed data
           line by line to the Word2Vec training method."""

        # If source is a list .txt of scraped urls:
        if self.source_type == "list":
            with open(self.source_path, mode="r", encoding="utf-8") as link_list:
                # Iterate trough urls:
                for link in link_list:
                    # Strip newline character.
                    link = link.rstrip()
                    # Call methods to download and handle file based on text format.
                    self.download_gz(link, self.temp_gz_file)
                    self.file_type_handling(self.temp_gz_file)
                    # Iterate through the text. One line one sentence.
                    for line in open(self.temp_text_file, mode="r", encoding="utf-8"):
                        # Tokenize sentence with simple_preprocess, import
                        # min. word length from config file.
                        sentence = utils.simple_preprocess(
                            line, min_len=config_file["Tokenizer"]["min-length"]
                        )
                        yield sentence

        # If source is a directory with downloaded files.
        elif self.source_type == "dir":
            # Iterate trough (gz) files:
            for file in scandir(self.source_path):
                if file.name.lower().endswith(".gz"):
                    # Call method to handle file based on on text format.
                    self.file_type_handling(file.path)
                    # Iterate through the text. One line one sentence.
                    for line in open(self.temp_text_file, mode="r", encoding="utf-8"):
                        # Tokenize sentence with simple_preprocess, import
                        # min. word length from config file.
                        sentence = utils.simple_preprocess(
                            line, min_len=config_file["Tokenizer"]["min-length"]
                        )
                        yield sentence

    def file_type_handling(self, file):
        """ Call appropriate functions based on corpus file type. """

        # Document is a preprepared .tsv with a "lemma" column.
        if ".tsv." in file:
            self.extract_gz(file, self.temp_tsv_file)
            self.convert_tsv(self.temp_tsv_file, self.temp_text_file)

        # If file is a plain text file.
        else:
            self.extract_gz(file, self.temp_text_file)

    def download_gz(self, url, out_file):
        """Download a .gz file."""
        filename = basename(url)
        print(f"Downloading {filename}.")
        urlretrieve(url, out_file)

    def extract_gz(self, gz_file, out_file):
        """Extract and save .gz file content."""
        filename = basename(gz_file)
        print(f"Uncompressing {filename}.")
        with gzip.open(gz_file, "r") as f_in, open(out_file, "wb") as f_out:
            copyfileobj(f_in, f_out)

    def convert_tsv(self, tsv_file, out_file):
        """Create a .txt file with continuous text from lemma column.
           One line = one sentence."""

        # Read .tsv file's lemma column to a pandas DataFrame.
        df = read_csv(tsv_file, engine="c", on_bad_lines="warn",
                      sep="\t", quoting=3, usecols=["lemma"])
        # Remove NaN rows.
        df.dropna(how="all", inplace=True)
        # Convert to list.
        df_list = list(df["lemma"])

        # Write words to out_file (min_length 3), add newline in place of sentence
        # closing punctuation.
        with open(out_file, mode="w+", encoding="utf-8") as f:
            for i in df_list:
                punct = [".", ";", "?", "!"]
                if len(i) > 2:
                    f.write(f"{i} ")
                elif i in punct:
                    f.write("\n")

class EpochSaver(CallbackAny2Vec):
    """Callback class to save trained model after each epoch."""
    # Convert!

    def __init__(self, model_path):
        """Object base attributes."""
        self.model_path = model_path
        self.epoch = 0 # Needed for filename.

    def on_epoch_end(self, model):
        """Called at the end of each epoch.
           Autosave temporary model files."""
        output_path = f"{self.model_path}_epoch{self.epoch}_autosave"
        model.save(output_path)
        self.epoch += 1
