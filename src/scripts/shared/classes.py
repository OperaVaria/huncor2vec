"""

classes.py

Python classes of the for the HunCor2Vec project.

"""

# Imports.
import gzip
from os import scandir
from os.path import basename
from shutil import copyfileobj
from urllib.request import urlretrieve
from gensim import utils
from gensim.test.utils import datapath
from pandas import read_csv
from .path_constants import TEMP_GZ_PATH, TEMP_TEXT_PATH, TEMP_TSV_PATH

class MyCorpus:
    """ Corpus object class. Feeds corpus data to model training iterator. """

    def __init__(self, source_type, source_path):
        """ Object base values. """
        self.source_type = source_type
        self.source_path = source_path
        self.temp_text_file = datapath(TEMP_TEXT_PATH)
        self.temp_tsv_file = datapath(TEMP_TSV_PATH)
        self.temp_gz_file = datapath(TEMP_GZ_PATH)

    def __iter__(self):
        """ Multi-file corpus iterator. """

        # If source is a list of scraped urls.
        if self.source_type == "list":
            with open(self.source_path, mode="r", encoding="utf-8") as link_list:
                for link in link_list:
                    link = link.rstrip()
                    self.download_gz(link, self.temp_gz_file)
                    self.file_type_handling(self.temp_gz_file)
                    for line in open(self.temp_text_file, mode="r", encoding="utf-8"):
                        yield utils.simple_preprocess(line)

        # If source is a directory with downloaded files.
        elif self.source_type == "dir":
            for file in scandir(self.source_path):
                if file.name.lower().endswith(".gz"):
                    self.file_type_handling(file.path)
                    for line in open(self.temp_text_file, mode="r", encoding="utf-8"):
                        yield utils.simple_preprocess(line)

    def file_type_handling(self, file):
        """ Call appropriate functions based on corpus file type. """
        # Document is a preprepared tsv with a "lemma" column.
        if ".tsv." in file:
            self.extract_gz(file, self.temp_tsv_file)
            self.convert_tsv(self.temp_tsv_file, self.temp_text_file)

        # If file is a plain text file.
        else:
            self.extract_gz(file, self.temp_text_file)

    def extract_gz(self, gz_file, out_file):
        """ Extract and save .gz file content. """
        filename = basename(gz_file)
        print(f"Uncompressing {filename}.")
        with gzip.open(gz_file, "r") as f_in, open(out_file, "wb") as f_out:
            copyfileobj(f_in, f_out)

    def download_gz(self, url, out_file):
        """ Download .gz file. """
        filename = basename(url)
        print(f"Downloading {filename}.")
        urlretrieve(url, out_file)

    def convert_tsv(self, tsv_file, out_file):
        """ Create continuous a text from lemma column to be read. """
        df = read_csv(tsv_file, engine="c", on_bad_lines="warn",
                      sep="\t", usecols=["lemma"])
        df.dropna(how="all", inplace=True)
        df_list = list(df["lemma"])
        with open(out_file, mode="w+", encoding="utf-8") as f:
            for i in df_list:
                if len(i) > 2:
                    f.write(f"{i} ")
                elif i == ".":
                    f.write("\n")
