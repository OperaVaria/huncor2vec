"""

Training.py

Training script to build a word2vec model.

Part of the HunCor2Vec project.

"""

# Imports:
import logging
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional, Tuple
from gensim.test.utils import datapath
from gensim.models import Word2Vec
from pick import pick

# Conditional imports (to be runnable as a stand-alone script):
if __name__ == "__main__":
    from shared.classes import MyCorpus, AutoSaver
    from shared.misc import (
        default_logging,
        check_dirs,
        error_crash,
        file_select_menu,
        load_config_file,
    )
    from shared.path_constants import (
        DOWNLOADS_DIR_PATH,
        LINKS_DIR_PATH,
        MODELS_DIR_PATH,
        TEMP_DIR_PATH,
        CONFIG_FILE_PATH,
    )
else:
    from tools.shared.classes import MyCorpus, AutoSaver
    from tools.shared.misc import (
        default_logging,
        check_dirs,
        error_crash,
        file_select_menu,
        load_config_file,
    )
    from tools.shared.path_constants import (
        DOWNLOADS_DIR_PATH,
        LINKS_DIR_PATH,
        MODELS_DIR_PATH,
        TEMP_DIR_PATH,
        CONFIG_FILE_PATH,
    )


def new_or_load() -> Tuple[Optional[str], Optional[str]]:
    """Ask user to train a completely new model file, or load an existing one
    and continue training. Returns model file path and the type of selected
    operation (new or load)."""

    # Menu variables.
    title = "Word2Vec Trainer\nSelect an option: "
    options = ["1. Train new model", "2. Load existing model", "3. Exit"]
    _, index = pick(options, title, indicator="=>", default_index=0)

    # Selection switch.
    match index:
        case 0:  # New
            operation_type = "new"
            new_model_name = input("Enter a name for the model: ")
            model_path = datapath((MODELS_DIR_PATH).joinpath(f"{new_model_name}.mdl"))
        case 1:  # Load
            operation_type = "load"
            model_path = datapath(
                file_select_menu("Select model file: ", MODELS_DIR_PATH, ".mdl")
            )
        case 2:  # Pass values to exit or return to main menu.
            return None, None
        case _:  # Incorrect selection (should not happen).
            error_crash("Selection error!")

    return operation_type, model_path


def get_training_source() -> Tuple[str, Path]:
    """Ask user for the type and location of the training sources. Returns the
    type of the source (list of file urls or a directory of downloaded
    files) and its path."""

    # Menu variables.
    title = "Select the type of training material: "
    options = ["1. Link list file", "2. Downloaded packages"]
    _, index = pick(options, title, indicator="=>", default_index=0)

    # Menu switch.
    match index:
        case 0:  # Link list
            source_type = "list"
            source_path = file_select_menu("Select list file: ", LINKS_DIR_PATH, ".txt")
        case 1:  # Downloaded files.
            source_type = "dir"
            source_path = DOWNLOADS_DIR_PATH
        case _:  # Incorrect selection (should not happen).
            source_type = None
            source_path = None
            error_crash("Selection error!")

    return source_type, source_path


def model_training(
    operation_type: str, model_path: str, source_type: str, source_path: Path
) -> Word2Vec:
    """Train model based on previous selections."""

    # Load settings from config.yml file
    config_file = load_config_file(CONFIG_FILE_PATH)
    word2vec_config = config_file["Word2Vec"]

    # Get number of CPU cores to set number of workers.
    cpu_core_num = cpu_count()

    # Initialize model autosave object.
    auto_save = AutoSaver(model_path)

    # Initialize and train new model.
    if operation_type == "new":
        sentences = MyCorpus(source_type, source_path)
        new_model = Word2Vec(
            sentences=sentences,
            callbacks=[auto_save],
            workers=cpu_core_num,
            **word2vec_config,
        )
        return new_model

    # Load and continue training model.
    if operation_type == "load":
        more_sentences = MyCorpus(source_type, source_path)
        loaded_model = Word2Vec.load(model_path)
        loaded_model.build_vocab(more_sentences, update=True)
        loaded_model.train(
            more_sentences,
            total_examples=loaded_model.corpus_count,
            epochs=loaded_model.epochs,
            callbacks=[auto_save],
            # vector_size=word2vec_config["vector_size"],
            # workers=cpu_core_num,
        )
        return loaded_model

    # Incorrect argument passed (should not happen).
    error_crash("Invalid argument passed!")
    return None


def main() -> None:
    """Main function."""

    logging.info("Launching the Word2Vec Trainer tool.")

    # Prompt for new model or continue to train existing.
    operation_type, model_path = new_or_load()

    # If a legitimate values are returned from new_or_load:
    # Set up training source.
    if operation_type and model_path:
        source_type, source_path = get_training_source()

    # If a legitimate source path is returned get_training_source:
    # Call training function.
    if source_path:
        model_training(operation_type, model_path, source_type, source_path)
        input("Press Enter to exit...")


# Run when launched as standalone script.
if __name__ == "__main__":
    # Set default logging settings.
    default_logging()
    # Check if necessary dirs exist.
    check_dirs([LINKS_DIR_PATH, MODELS_DIR_PATH, TEMP_DIR_PATH])
    # Launch main function.
    main()
    # Ending message.
    logging.info("Exiting...")
