"""

main.py

Main file of the HunCor2Vec project.

TODO: 1. Error handling.
      2. More query tasks.
      3. Better docstrings.
      4. Documentation.
      5. Possible GUI.

"""

# Imports:
from sys import exit as sys_exit
from pick import pick
from scripts.scraping import main as scraping
from scripts.downloading import main as downloading
from scripts.training import main as training
from scripts.querying import main as querying
from scripts.shared.path_constants import LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH
from scripts.shared.misc import check_dirs


def module_menu():
    """ Task select menu. """
    title = "Word2Vec tool.\nSelect task: "
    options = ["1. Scraping", "2. Downloading", "3. Training", "4. Querying", "5. Exit"]
    _, index = pick(options, title, indicator='=>', default_index=0)
    match index:
        case 0: # Launch scraper script.
            scraping()
        case 1: # Launch download script.
            downloading()
        case 2: # Launch trainer script.
            training()
        case 3: # Launch query script.
            querying()
        case 4:
            # Exit app.
            sys_exit(0)
        case _:
            # Incorrect selection (should not happen).
            print("Selection error!")
            sys_exit(1)


def main():
    """ Main function. """

    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH])

    # Launch app main loop.
    while True:
        module_menu()


# Run main function.
if __name__ == '__main__':
    main()
