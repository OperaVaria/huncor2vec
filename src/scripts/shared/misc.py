"""

misc.py

Miscellaneous auxiliary functions of the HunCor2Vec project.

"""

# Imports.
from os import scandir
from os.path import isfile
from pick import pick


def check_dirs(dirs):
    """ Check if required directories exist,
        if not, create them."""
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def file_select_loop(prompt, dir_path):
    """ Prompt loop to select an existing file inside
        a given directory. """
    while True:
        file_name = input(prompt)
        file_path = (dir_path).joinpath(file_name)
        if isfile(file_path):
            break
        print("File does not exist!")
    return file_path


def file_select_menu(prompt, dir_path, file_ext):
    """ Create a pick menu to select a file from
        a given directory.
        Filters based on file extension.
        Returns selected file path. """
    title = prompt
    options = []
    for file in scandir(dir_path):
        if file.name.lower().endswith(file_ext):
            options.append(file.name)
    option, _ = pick(options, title, indicator='=>', default_index=0)
    selected_file = (dir_path).joinpath(option)
    return selected_file


# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
