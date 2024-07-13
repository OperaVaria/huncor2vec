"""

scraper.py

Corpus file list scraper for the Hungarian Webcorpus 2.0.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from re import compile as re_compile
from sys import exit as sys_exit
import requests
from bs4 import BeautifulSoup
from pick import pick

# Conditional imports (to be runnable as a standalone script):
if __name__ == "__main__":
    from shared.path_constants import LINKS_DIR_PATH
else:
    from scripts.shared.path_constants import LINKS_DIR_PATH

# Configure logging
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

def corpus_select_menu():
    """Corpus select menu. Sets up corpus url and output file name, calls scraping function."""

    title = "Webcorpus 2.0 scraper\nSelect corpus: "
    options = ["1. text (25GB)", "2. clean (83GB)", "3. ana (511GB)", "4. Exit"]

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
                logging.error("selection error!")
                sys_exit(1)

        # Create full path for link list file.
        list_file_path = LINKS_DIR_PATH.joinpath(list_filename)
        # Call scraping function.
        webcorpus2_scraping(corpus_url, list_file_path)


def webcorpus2_scraping(corpus_url, out_file):
    """Scrape selected webcorpus2 website for document links.
    File url list saved to links/, single url/line format."""

    print("Scraping...")

    # Get website, raise error and notify if unsuccessful.
    try:
        res = requests.get(url=corpus_url, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e_req:
        logging.error("request failed: %s", e_req)
        return

    # Parse with BeautifulSoup.
    soup = BeautifulSoup(res.text, "html.parser")

    # If does not exist, create links/ dir.
    LINKS_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # Find and write only the .gz file links to the out_file.
    with open(file=out_file, mode="w+", encoding="utf-8") as my_file:
        for link in soup.find_all("a", string=re_compile(".gz")):
            gz_url = link.get("href")
            my_file.write(f"{corpus_url}{gz_url}\n")

    # End prompts.
    logging.info("process Done. Saved to %s", out_file)
    input("Press Enter to return...")


def main():
    """Main function."""

    print("\nWebcorpus 2.0 scraper\n")

    # Launch menu.
    corpus_select_menu()


# Run when launched as standalone script.
if __name__ == "__main__":
    main()
    print("Exiting...")
