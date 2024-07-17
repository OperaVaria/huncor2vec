"""

main.py

Main file of the HunCor2Vec project.

This small command line app provides automation tools to easily
retrieve material form the Hungarian Webcorpus 2.0, train a Word2Vec
model with the said texts, and evaluate the results.

TODO: 1. Testing
      3. Possible GUI

"""

# Imports:
import logging
from pick import pick
from tools.scraping import main as scraping
from tools.downloading import main as downloading
from tools.training import main as training
from tools.querying import main as querying
from tools.shared.path_constants import LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH
from tools.shared.misc import default_logging, check_dirs, error_crash

# Metadata variables:
__author__ = "OperaVaria"
__contact__ = "lcs_it@proton.me"
__version__ = "1.0.0"
__date__ = "2024.07.17"

# License:
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


def tools_menu() -> None:
    """Tool select menu. Calls the main function of the appropriate script."""

    # Menu variables.
    title = "HunCor2Vec Toolset\nSelect a task: "
    options = ["1. Scraping", "2. Downloading", "3. Training", "4. Querying", "5. Exit"]

    # Menu loop.
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
                error_crash("Selection error!")


def main() -> None:
    """Main function."""
    logging.info("Launching the HunCor2Vec toolset.")
    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH])
    # Launch main menu.
    tools_menu()


# Run when launched as a script:
if __name__ == "__main__":
    # Set default logging settings.
    default_logging()
    # Launch main function.
    main()
    # Ending message.
    logging.info("Exiting...")
