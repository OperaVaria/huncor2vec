"""

scraper.py

Corpus file list scraper for the Hungarian Webcorpus 2.0.

Part of the HunCor2Vec project.

"""

# Imports.
from re import compile as re_compile
from sys import exit as sys_exit
import requests
from bs4 import BeautifulSoup
from pick import pick

# Conditional imports (to be runnable as a standalone script).
if __name__ == '__main__':
    from shared.path_constants import LINKS_DIR_PATH
else:
    from scripts.shared.path_constants import LINKS_DIR_PATH


def corpus_select_menu():
    """ Corpus select menu. Sets up corpus url and output file name. """
    title = "Webcorpus 2.0 scraper\nSelect corpus: "
    options = ["1. text (25GB)", "2. clean (83GB)", "3. ana (511GB)", "4. exit"]
    _, index = pick(options, title, indicator='=>', default_index=0)
    match index:
        case 0: # Standard text corpus.
            corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_text/"
            filename = "list_webcor2_text.txt"
        case 1: # Cleaned and lemmatised corpus.
            corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_clean/"
            filename = "list_webcor2_clean.txt"
        case 2: # Corpus with lemma and morphological analysis added.
            corpus_url = "https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2/"
            filename = "list_webcor2_ana.txt"
        case 3: # Pass values to exit or return to main menu.
            return None, None
        case _: # Incorrect selection (should not happen).
            print("Selection error!")
            sys_exit(1)
    return corpus_url, filename


def webcorpus2_scraping(corpus_url, out_file):
    """ Scrape selected webcorpus2 website for document links.
        File url list saved to links/, single url/line format. """

    print("Scraping...")

    # Get website.
    grab = requests.get(url=corpus_url, timeout=10)
    if grab.ok is not True:
        return grab.raise_for_status()

    # Parse with bs4.
    soup = BeautifulSoup(grab.text, "html.parser")

    # If does not exist, create links/ dir.
    LINKS_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # Write only file links to out_file.
    with open(file=out_file, mode="w+", encoding="utf-8") as my_file:
        for link in soup.find_all("a", string=re_compile(".gz")):
            gz_url = link.get("href")
            my_file.write(f"{corpus_url}{gz_url}\n")

    print(f"Process Done. Saved to {out_file}")
    return input("Press Enter to continue...")


def main():
    """ Main function. """

    # Call menu function.
    corpus_url, list_filename = corpus_select_menu()

    # If legitime, non exit option selected,
    # call scraping function.
    if corpus_url is not None:
        list_file_path = (LINKS_DIR_PATH).joinpath(list_filename)
        webcorpus2_scraping(corpus_url, list_file_path)

    # else (corpus_url = None): exit or return to main menu.


# Run when launched as standalone script.
if __name__ == '__main__':
    main()
    print("Exiting...")
