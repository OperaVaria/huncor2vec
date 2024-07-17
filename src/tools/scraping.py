"""

scraper.py

Corpus file list scraper for the Hungarian Webcorpus 2.0.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from re import compile as re_compile
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pick import pick

# Conditional imports (to be runnable as a standalone script):
if __name__ == "__main__":
    from shared.misc import check_dirs, default_logging, error_crash
    from shared.path_constants import LINKS_DIR_PATH
else:
    from tools.shared.misc import check_dirs, default_logging, error_crash
    from tools.shared.path_constants import LINKS_DIR_PATH


def corpus_select_menu() -> None:
    """Corpus select menu. Sets up corpus url and output file name, calls scraping function."""

    # Menu variables.
    title = "Webcorpus 2.0 Scraper\nSelect a corpus: "
    options = ["1. text (25GB)", "2. clean (83GB)", "3. ana (511GB)", "4. Exit"]

    # Menu loop.
    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:  # Standard text corpus.
                corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_text/"
                list_filename = "list_webcor2_text.txt"
            case 1:  # Cleaned and lemmatized corpus.
                corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_clean/"
                list_filename = "list_webcor2_clean.txt"
            case 2:  # Corpus with lemma and morphological analysis added.
                corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2/"
                list_filename = "list_webcor2_ana.txt"
            case 3:  # Break out of menu loop
                break
            case _:  # Incorrect selection (should not happen).
                error_crash("Selection error!")

        # Create full path for the link list file.
        list_file_path = LINKS_DIR_PATH.joinpath(list_filename)
        # Call scraping function.
        webcorpus2_scraping(corpus_url, list_file_path)


def webcorpus2_scraping(corpus_url: str, out_file: Path) -> None:
    """Scrape selected Webcorpus 2.0 website for document links.
    File url list saved to links/, single url/line format."""

    logging.info("Scraping...")

    # Get website, if request fails, raise error and notify.
    try:
        res = requests.get(url=corpus_url, timeout=10)
        res.raise_for_status()
    except requests.RequestException as err_req:
        logging.error("Request failed: %s", err_req)
        input("Press Enter to return...")
        return

    # Parse with BeautifulSoup.
    soup = BeautifulSoup(res.text, "html.parser")

    # Find and write only the .gz file links to the out_file.
    with open(file=out_file, mode="w+", encoding="utf-8") as my_file:
        for link in soup.find_all("a", string=re_compile(".gz")):
            gz_url = link.get("href")
            my_file.write(f"{corpus_url}{gz_url}\n")

    # Operation end prompt.
    logging.info("Process Done. Saved to %s", out_file)
    input("Press Enter to return...")


def main() -> None:
    """Main function."""
    logging.info("Launching the Webcorpus 2.0 Scraper tool.")
    # Launch menu.
    corpus_select_menu()


# Run when launched as standalone script.
if __name__ == "__main__":
    # Set default logging settings.
    default_logging()
    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH])
    # Launch main function.
    main()
    # Ending message.
    logging.info("Exiting...")
