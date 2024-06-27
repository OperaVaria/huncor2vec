"""

Training.py

Training script to build a word2vec model.

Part of the HunCor2Vec project.

"""

# Imports.
import logging
from sys import exit as sys_exit
from gensim.test.utils import datapath
from gensim.models import Word2Vec
from pick import pick

# Conditional imports (to be runnable as a stand-alone script).
if __name__ == "__main__":
    from shared.classes import MyCorpus
    from shared.misc import file_select_menu
    from shared.path_constants import (
        DOWNLOADS_DIR_PATH,
        LINKS_DIR_PATH,
        MODELS_DIR_PATH,
    )

else:
    from scripts.shared.classes import MyCorpus
    from scripts.shared.misc import file_select_menu
    from scripts.shared.path_constants import (
        DOWNLOADS_DIR_PATH,
        LINKS_DIR_PATH,
        MODELS_DIR_PATH,
    )



def new_or_load():
    """ Ask user to train completely new model file, or load existing one
        and continue training. """
    title = "Word2Vec trainer\nSelect option: "
    options = ["1. Train new model", "2. Load existing model", "3. Exit"]
    _, index = pick(options, title, indicator='=>', default_index=0)
    match index:
        case 0: # New
            new_model_name = input("Enter a name for the model: ")
            model_path = datapath((MODELS_DIR_PATH).joinpath(f"{new_model_name}.mdl"))
            operation_type = "new"
        case 1: # Load
            model_path = datapath(file_select_menu("Select model file: ", MODELS_DIR_PATH, ".mdl"))
            operation_type = "load"
        case 2: # Pass values to exit or return to main menu.
            return None, None
        case _:
            # Incorrect selection (should not happen).
            print("Selection error!")
            sys_exit(1)
    return operation_type, model_path


def get_training_source():
    """ Ask user for type and location of training source"""
    title = "Select the type of training material: "
    options = ["1. Link list file", "2. Downloaded packages"]
    _, index = pick(options, title, indicator='=>', default_index=0)
    match index:
        case 0: # Link list.
            # Setup file path.
            source_path = file_select_menu("Select list file: ", LINKS_DIR_PATH, ".txt")
            source_type = "list"
        case 1: # Downloaded files.
            # Select model.
            source_path = DOWNLOADS_DIR_PATH
            source_type = "dir"
        case _:
            # Incorrect selection (should not happen).
            print("Selection error!")
            sys_exit(1)
    return source_type, source_path


def model_training(operation_type, model_path, source_type, source_path):
    """ Train model based on previous selections. """

    # Initialize and train new model.
    if operation_type == "new":
        sentences = MyCorpus(source_type, source_path)
        new_model = Word2Vec(sentences=sentences)
        print("Training complete.")
        return new_model

    # Load and continue training model.
    if operation_type == "load":
        more_sentences = MyCorpus(source_type, source_path)
        loaded_model = Word2Vec.load(model_path)
        loaded_model.build_vocab(more_sentences, update=True)
        loaded_model.train(more_sentences, total_examples=loaded_model.corpus_count,
                            epochs=loaded_model.epochs)
        return loaded_model

    # Incorrect argument passed (should not happen).
    print("Error!")
    sys_exit(1)


def main():
    """ Main function. """

    # Configure logging.
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # Prompt for new model or continue to train existing.
    operation_type, model_path = new_or_load()

    # If legitime, non exit option selected,
    # continue operation.
    if operation_type is not None:

        # Set up training source.
        source_type, source_path = get_training_source()

        # Call training function.
        model = model_training(operation_type, model_path, source_type, source_path)

        # Save model.
        model.save(model_path)
        print("Model saved.")
        input("\nPress Enter to continue...")

    # else (operation_type = None): exit or return to main menu.


# Run main function.
if __name__ == '__main__':
    main()
    print("Exiting...")
