import re

class Dictionnary:
    """
    Stores the elements of an Frelatage dictionary. 
    """
    def __init__(self) -> None:
        self.dictionnary = []
        # dict_element="myelement" -> "myelement"
        self.DICTIONNARY_ELEMENT_REGEXP = r'".+"'

    def load_dictionnary_from_file(self, filename) -> list:
        """
        Read a Frelatage dictionnary file and extract dictionnary elements from it
        """
        file_dictionnary = []

        with open(filename, "r") as f:
            lines = [line.replace("\n", "").strip() for line in f.readlines()]

            for line in lines:
                # Skip empty lines and commentaries
                if not line or line[0] == "#":
                    continue
                # Parse line
                dictionnary_element = re.findall(self.DICTIONNARY_ELEMENT_REGEXP, line)
                if dictionnary_element:
                    # Remove the quote from both the beginning and the end
                    dictionnary_element = dictionnary_element[0][1:-1]
                    file_dictionnary.append(dictionnary_element)
        return file_dictionnary