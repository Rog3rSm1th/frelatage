import os
import shutil


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

        # Files located in the input folder that are used in this stage
        filenames = [
            file_argument.value
            for file_argument in filter(
                lambda a: a.file, self.queue.current_arguments()
            )
        ]
        # Copy the useful files into the subdirectory
        for i in range(len(filenames)):
            # /tmp/frelatage/<thread>/<argument position>
            argument_directory = os.path.join(thread_directory, str(i))
            os.makedirs(argument_directory)
            # ./in/<any subfolder>/<filename>
            input_file = os.path.join(start_input_directory, filenames[i])
            # /tmp/frelatage/<thread>/<argument position>/<filename>
            output_file = os.path.join(
                argument_directory, os.path.basename(filenames[i])
            )
            shutil.copyfile(input_file, output_file)
    return True


def init_file_input_arguments(self) -> bool:
    """
    Initialization of the file arguments values.

    Input {
        type: File
        value: <input_file_tmp_dir>/<thread 0>/<argument position>/<filename>
    }
    """
    file_input_arguments_count = 0
    # We initialize the value of each argument of type "file".
    for i in range(len(self.arguments)):
        if self.arguments[i].file:
            # <input_file_tmp_dir>/<thread 0>/<argument position>/<filename>
            self.arguments[
                i
            ].value = "{base_directory}/{thread}/{position}/{filename}".format(
                base_directory=self.config.FRELATAGE_INPUT_FILE_TMP_DIR,
                thread="0",
                position=str(i),
                filename=os.path.basename(self.arguments[i].value),
            )
            file_input_arguments_count += 1
    return True


def init_file_inputs(self) -> bool:
    """
    Set up the tree structure to fuzz a function with "file" type arguments
    """
    if any([argument.file for argument in self.arguments]):
        self.init_input_folder()
        self.init_file_input_arguments()
