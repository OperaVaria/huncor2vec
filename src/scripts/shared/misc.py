"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
from os import scandir
from os.path import isfile
from gensim.test.utils import datapath
from pick import pick


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

def file_select_menu(prompt, folder, extension):
    """ Create a menu to select a file from a directory.
        Filters based on file extension.
        Returns selected file path. """
    title = prompt
    options = []
    for file in scandir(folder):
        if file.name.lower().endswith(extension):
            options.append(file.name)
    option, _ = pick(options, title, indicator='=>', default_index=0)
    selected_file = (folder).joinpath(option)
    return selected_file



# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
