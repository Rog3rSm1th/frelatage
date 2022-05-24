import glob
import os
from frelatage.dictionary.dictionary import Dictionary


def load_dictionary(dictionary_folder: str) -> bool:
    """
    Load all the dictionaries from the dictionary folder
    """
    dictionary = Dictionary()
    dictionaries = []
    if os.path.isdir(dictionary_folder):
        # find all ".dict" files in the dictionary folder
        dictionary_files = glob.glob(os.path.join(dictionary_folder, "*.dict"))
        for file in dictionary_files:
            # parse dictionary files
            dictionaries += dictionary.load_dictionary_from_file(file)
    return dictionaries
