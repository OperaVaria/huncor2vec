"""

querying.py

Script to query a trained word2vec model.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from pprint import pprint
from sys import exit as sys_exit
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from pick import pick

# Conditional imports (to be runnable as a stand-alone script):
if __name__ == "__main__":
    from shared.misc import file_select_menu
    from shared.path_constants import MODELS_DIR_PATH
else:
    from scripts.shared.misc import file_select_menu
    from scripts.shared.path_constants import MODELS_DIR_PATH

# Configure logging
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

def query_task_menu(model):
    """Menu to select appropriate query task."""

    title = "Select task: "
    options = [
        "1. Similarity between two words",
        "2. List the five most similar words",
        "3. Find the word that does not belong in the sequence",
        "4. Exit",
    ]

    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:
                two_words_similarity(model)
            case 1:
                five_most_similar(model)
            case 2:
                does_not_match(model)
            case 3:  # Break loop: exit script or return to main menu.
                break
            case _:  # Incorrect selection (should not happen).
                logging.error("selection error!")
                sys_exit(1)


def two_words_similarity(model):
    """Calculate the similarity between two words."""
    word1 = input("\nEnter word #1: ")
    word2 = input("Enter word #2: ")
    try:
        similarity = model.wv.similarity(word1, word2)
        print(f"\nSimilarity: {similarity}")
    except KeyError as e_two_sim:
        logging.error("Word not in vocabulary: %s", e_two_sim)
        print("\nError: One or both words not in vocabulary.")
    input("\nPress Enter to return...")


def five_most_similar(model):
    """List five most similar words to input."""
    word = input("\nEnter word: ")
    try:
        similar_words = model.wv.most_similar(word, topn=5)
        pprint(similar_words)
    except KeyError as e_five_sim:
        logging.error("Word not in vocabulary: %s", e_five_sim)
        print("\nError: Word not in vocabulary.")
    input("\nPress Enter to return...")


def does_not_match(model):
    """Find the word that does not match the rest."""
    words = input("\nEnter words (separated by space): ").split()
    try:
        mismatch = model.wv.doesnt_match(words)
        print(f"Mismatch: {mismatch}")
    except KeyError as e_match:
        logging.error("One or more words not in vocabulary: %s", e_match)
        print("\nError: One or more words not in vocabulary.")
    input("\nPress Enter to return...")


def main():
    """Main function."""

    # Ask for model file name and load.
    model_path = datapath(
        file_select_menu(
            "Word2Vec model querying tool\nSelect model file: ",
            MODELS_DIR_PATH,
            ".mdl",
        )
    )
    print(f"Loading {model_path}...")
    model = Word2Vec.load(model_path)

    # Launch menu.
    query_task_menu(model)


# Run main function.
if __name__ == "__main__":
    main()
    print("Exiting...")
