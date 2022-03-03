from distutils.dir_util import copy_tree
import shutil
import glob
import os

def init_input_folder(self) -> bool:
    """
    Creating the tree structure for temporary files storage.
    By default it will be located in /tmp/frelatage
    """
    start_input_directory = self.input_directory
    tmp_input_directory = self.config.FRELATAGE_INPUT_FILE_TMP_DIR

    # Create /tmp/frelatage (default value) directory if not exists
    if not os.path.exists(tmp_input_directory):
        os.makedirs(tmp_input_directory)

    # Empty the directory
    else:
        list_dir = os.listdir(tmp_input_directory)
        for filename in list_dir:
            file_path = os.path.join(tmp_input_directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Create a subdirectory /tmp/frelatage/<subfolder> for each thread
    for thread in range(self.threads_count):
        thread_directory = os.path.join(tmp_input_directory, str(thread))
        os.makedirs(thread_directory)
        # Copy the input folder content into the subdirectory
        copy_tree(start_input_directory, thread_directory)
    return True

def init_file_input_arguments(self) -> bool:
    """
    Initialization of the file arguments value.

    Input {
        type: File
        value: <input_file_tmp_dir>/<thread 0>/<filename>
    }
    """
    file_input_arguments_count = 0
    # We initialize the value of each argument of type "file".
    for argument in self.arguments:
        if argument.file:
            # <input_file_tmp_dir>/<thread 0>/<filename>
            argument.value = "{base_directory}/{thread}/{file_input_arguments_count}".format(
                base_directory=self.config.FRELATAGE_INPUT_FILE_TMP_DIR,
                thread="0",
                file_input_arguments_count=file_input_arguments_count, 
            )
            file_input_arguments_count+= 1
    return True

def init_file_inputs(self) -> bool:
    """
    Set up the tree structure to fuzz a function with "file" type arguments
    """
    if all([argument.file for argument in self.arguments]):
        self.init_input_folder()
        self.init_file_input_arguments()