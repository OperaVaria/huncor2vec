""" 

querying.py

Script to query a trained word2vec model.

Part of the HunCor2Vec project.

"""

# Imports.
from pprint import pprint
from sys import exit as sys_exit
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from pick import pick

# Conditional imports (to be runnable as a stand-alone script).
if __name__ == '__main__':
    from shared.misc import file_select_menu
    from shared.path_constants import MODELS_DIR_PATH
else:
    from scripts.shared.misc import file_select_menu
    from scripts.shared.path_constants import MODELS_DIR_PATH


def query_task_menu(model):
    """ Menu to select appropriate query task. Looped. """
    title = "Select task: "
    options = ["1. Similarity between two words",
               "2. List the five most similar words",
               "3. Find the word that does not belong in the sequence",
               "4. Exit"]
    query_task_loop = True
    while query_task_loop is True:
        _, index = pick(options, title, indicator='=>', default_index=0)
        match index:
            case 0:
                two_words_similarity(model)
            case 1:
                five_most_similar(model)
            case 2:
                does_not_match(model)
            case 3: # Break loop, exit script or return to main menu.
                query_task_loop = False
            case _: # Incorrect selection (should not happen).
                print("Selection error!")
                sys_exit(1)

def two_words_similarity(model):
    """ Calculate the similarity between two words. """
    word1 = input("\nEnter word #1: ")
    word2 = input("Enter word #2: ")
    print(f"\nSimilarity: {model.wv.similarity(word1, word2)}")
    input("\nPress Enter to return...")

def five_most_similar(model):
    """ List five most similar words to input. """
    word = input("\nEnter word: ")
    pprint(model.wv.most_similar(word, topn=5))
    input("\nPress Enter to return...")

def does_not_match(model):
    """ Find the word that does not match from input. """
    words = list(input("\nEnter words: ").split())
    print(f"Mismatch: {model.wv.doesnt_match(words)}")
    input("\nPress Enter to return...")

def main():
    """ Main function. Ask for model filename, load model, and
        run select menu. """
    model_path = datapath(file_select_menu(
        "Word2Vec model querying tool\n\nSelect model file: ", MODELS_DIR_PATH, ".mdl"
    ))
    print(f"Loading {model_path}...")
    model = Word2Vec.load(model_path)
    query_task_menu(model)

# Run main function.
if __name__ == '__main__':
    main()
    print("Exiting...")
