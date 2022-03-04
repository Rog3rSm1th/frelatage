import sys
import os 

class Config:
    """
    We can pass configuration through environnement variables
    """
    # Enable the use of mutations based on dictionnary elements
    FRELATAGE_DICTIONNARY_ENABLE = True if os.getenv('FRELATAGE_DICTIONNARY_ENABLE', "1") == "1" else False
    # Delay after which a function will return a timeoutError
    FRELATAGE_TIMEOUT_DELAY = int(os.getenv('TIMEOUT_DELAY', 2))
    # Temporary folder where input files are stored. 
    # Need to be an absolute path
    FRELATAGE_INPUT_FILE_TMP_DIR = str(os.getenv('FRELATAGE_INPUT_FILE_TMP_DIR', '/tmp/frelatage'))
    # Maximum size of an input variable
    FRELATAGE_INPUT_MAX_LEN = int(os.getenv('FRELATAGE_INPUT_MAX_LEN', 4096))
    # Maximum number of simultaneous threads
    FRELATAGE_MAX_THREADS = int(os.getenv('FRELATAGE_MAX_THREADS', 20))
    # Default directory for dictionaries
    # Relative path (to the path of the fuzzing file)
    FRELATAGE_DICTIONNARY_DIR = str(os.path.join(
                                        os.path.dirname(os.path.realpath(sys.argv[0])),
                                        os.getenv('FRELATAGE_DICTIONNARY_DIR', "./dict")
                                ))