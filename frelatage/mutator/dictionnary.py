from frelatage.dictionnary.dictionnary import Dictionnary
import glob
import os

def load_dictionnary(dictionnary_folder: str) -> bool:
    """
    Load all the dictionnaries from the dictionnary folder
    """
    dictionnary = Dictionnary()
    dictionnaries = []
    if os.path.isdir(dictionnary_folder):
        # find all ".dict" files in the dictionnary folder
        dictionnary_files = glob.glob(os.path.join(dictionnary_folder, "*.dict"))
        for file in dictionnary_files:
            # parse dictionnary files
            dictionnaries += dictionnary.load_dictionnary_from_file(file)
    return dictionnaries