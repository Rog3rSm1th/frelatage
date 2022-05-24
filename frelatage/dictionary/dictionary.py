import re


class Dictionary:
    """
    Stores the elements of an Frelatage dictionary.
    """

    def __init__(self) -> None:
        self.dictionary = []
        # dict_element="myelement" -> "myelement"
        self.DICTIONARY_ELEMENT_REGEXP = r'".+"'

    def load_dictionary_from_file(self, filename) -> list:
        """
        Read a Frelatage dictionary file and extract dictionary elements from it
        """
        file_dictionary = []

        with open(filename, "r") as f:
            lines = [line.replace("\n", "").strip() for line in f.readlines()]

            for line in lines:
                # Skip empty lines and commentaries
                if not line or line[0] == "#":
                    continue
                # Parse line
                dictionary_element = re.findall(self.DICTIONARY_ELEMENT_REGEXP, line)
                if dictionary_element:
                    # Remove the quote from both the beginning and the end
                    dictionary_element = dictionary_element[0][1:-1]
                    file_dictionary.append(dictionary_element)
        return file_dictionary
