"""

main.py

Main file of the HunCor2Vec project.

This small command line app provides automation tools to easily
retrieve material form the Hungarian Webcorpus 2.0, train a Word2Vec
model with the said texts, and evaluate the results.

TODO: 1. Error handling.
      2. More query tasks.
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

# Metadata variables:
__author__ = "OperaVaria"
__contact__ = "lcs_it@proton.me"
__version__ = "0.0.0"
__date__ = "2024.xx.xx"

# Licence:
__license__ = "GPLv3"
__copyright__ = "Copyright © 2024, Csaba Latosinszky"

"""
This program is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>
"""


def task_menu():
    """Task select menu. Calls main function of appropriate script."""

    title = "HunCor2Vec toolset\nSelect task: "
    options = ["1. Scraping", "2. Downloading", "3. Training", "4. Querying", "5. Exit"]

    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:  # Launch scraper script.
                scraping()
            case 1:  # Launch download script.
                downloading()
            case 2:  # Launch trainer script.
                training()
            case 3:  # Launch query script.
                querying()
            case 4:  # Break loop, exit app.
                break
            case _:  # Incorrect selection (should not happen).
                print("Selection error!")
                sys_exit(1)


def main():
    """Main function."""

    print("\nHunCor2Vec toolset\n")

    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH])

    # Launch main menu.
    task_menu()

    print("Exiting...")


# Run main function.
if __name__ == "__main__":
    main()
