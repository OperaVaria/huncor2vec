"""

querying.py

Script to query a trained word2vec model.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from pprint import pprint
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from pick import pick

# Conditional imports (to be runnable as a stand-alone script):
if __name__ == "__main__":
    from shared.misc import check_dirs, default_logging, error_crash, file_select_menu
    from shared.path_constants import MODELS_DIR_PATH
else:
    from tools.shared.misc import check_dirs, default_logging, error_crash, file_select_menu
    from tools.shared.path_constants import MODELS_DIR_PATH


def query_task_menu(model: Word2Vec) -> None:
    """Menu to select appropriate query task."""

    # Menu variables.
    title = "Select task: "
    options = [
        "1. Similarity between two words",
        "2. List the five most similar words",
        "3. Find the word that does not belong in the sequence",
        "4. Exit",
    ]

    # Menu loop.
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
                error_crash("Selection error!")


def two_words_similarity(model: Word2Vec) -> None:
    """Calculate the similarity between two words."""
    word1 = input("\nEnter word #1: ")
    word2 = input("Enter word #2: ")
    try:
        similarity = model.wv.similarity(word1, word2)
        print(f"\nSimilarity: {similarity}")
    except KeyError as err_two_sim:
        logging.error("Word not in vocabulary: %s", err_two_sim)
    input("Press Enter to return...")


def five_most_similar(model: Word2Vec) -> None:
    """List five most similar words to input."""
    word = input("\nEnter word: ")
    try:
        similar_words = model.wv.most_similar(word, topn=5)
        pprint(similar_words)
    except KeyError as err_five_sim:
        logging.error("Word not in vocabulary: %s", err_five_sim)
    input("Press Enter to return...")


def does_not_match(model: Word2Vec) -> None:
    """Find the word that does not match the rest."""
    words = input("\nEnter words (separated by space): ").split()
    try:
        mismatch = model.wv.doesnt_match(words)
        print(f"Mismatch: {mismatch}")
    except KeyError as err_match:
        logging.error("One or more words not in vocabulary: %s", err_match)
    input("\nPress Enter to return...")


def main() -> None:
    """Main function."""

    logging.info("Launching the Word2Vec model querying tool.")

    # Ask for model file name and load.
    model_path = file_select_menu(
        "Word2Vec Query\nSelect model file: ",
        MODELS_DIR_PATH,
        ".mdl",
    )

    # Only continue operations if a legitimate file was selected.
    if model_path:
        # Create model instance
        model = Word2Vec.load(datapath(model_path))
        # Launch menu.
        query_task_menu(model)


# Run when launched as standalone script.
if __name__ == "__main__":
    # Set default logging settings.
    default_logging()
    # Check if necessary dirs exist.
    check_dirs([MODELS_DIR_PATH])
    # Launch main function.
    main()
    # Ending message.
    logging.info("Exiting...")
