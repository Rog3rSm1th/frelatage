from frelatage.config.config import Config
from frelatage.input.input import Input 
import glob
import sys
import os

def load_corpus(directory: str, file_extensions: list = []) -> list[Input]:
    """
    Load a corpus from a file input directory subdirectory.
    Return a list of inputs.
    """
    inputs = []

    # ./<input directory>/<subdirectory>
    input_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            Config.FRELATAGE_INPUT_DIR,
            directory
    )

    # Search for file inputs in the subdirectory
    if not file_extensions:
        file_inputs = glob.glob(os.path.join(input_directory, "*"))
    # filter file inputs by extension
    else:
        file_inputs = []
        for file_extension in file_extensions:
            file_inputs += glob.glob(os.path.join(input_directory, "*.{extension}".format(extension=file_extension)))

    # Relative path
    file_inputs = [os.path.relpath(file_input, input_directory) for file_input in file_inputs]

    # Create an Input object for every file in the subdirectory
    for file_input in file_inputs:
        inputs.append(Input(file=True, value=file_input))
    return inputs