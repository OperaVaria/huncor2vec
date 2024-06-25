"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
from os.path import isfile
from gensim.test.utils import datapath


def check_dirs(dirs):
    """ Check if required directories exist,
        if not, create them."""
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def file_select_loop(prompt, folder):
    """ Prompt loop to select an existing file. """
    while True:
        file_name = input(prompt)
        file_path = datapath((folder).joinpath(file_name))
        if isfile(file_path):
            break
        print("File does not exist!")
    return file_path


# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
