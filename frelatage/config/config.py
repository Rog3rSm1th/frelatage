import math
import os
import sys


class FrelatageConfigError(Exception):
    pass


class Config:
    """
    We can pass configuration through environnement variables
    """

    # Enable the use of mutations based on dictionary elements
    if os.getenv("FRELATAGE_DICTIONARY_ENABLE", "1") not in ("1", "0"):
        raise FrelatageConfigError("FRELATAGE_DICTIONARY_ENABLE must '1' or '0'")
    FRELATAGE_DICTIONARY_ENABLE = (
        True if os.getenv("FRELATAGE_DICTIONARY_ENABLE", "1") == "1" else False
    )

    # Save coverage increase reports to reuse them later
    if os.getenv("FRELATAGE_SAVE_NEW_COVERAGE", "1") not in ("1", "0"):
        raise FrelatageConfigError("FRELATAGE_SAVE_NEW_COVERAGE must '1' or '0'")
    FRELATAGE_SAVE_NEW_COVERAGE = (
        True if os.getenv("FRELATAGE_SAVE_NEW_COVERAGE", "1") == "1" else False
    )

    # Enable the debug mode
    if os.getenv("FRELATAGE_DEBUG_MODE", "1") not in ("1", "0"):
        raise FrelatageConfigError("FRELATAGE_DEBUG_MODE must '1' or '0'")
    FRELATAGE_DEBUG_MODE = (
        True if os.getenv("FRELATAGE_DEBUG_MODE", "1") == "1" else False
    )

    # Delay in seconds after which a function will return a timeoutError
    # Must be greater than 1
    if not 1 <= int(os.getenv("FRELATAGE_TIMEOUT_DELAY", 2)) <= math.inf:
        raise FrelatageConfigError("FRELATAGE_TIMEOUT_DELAY must be greater than 1")
    FRELATAGE_TIMEOUT_DELAY = int(os.getenv("FRELATAGE_TIMEOUT_DELAY", 2))

    # Temporary folder where input files are stored.
    # Need to be an absolute path
    FRELATAGE_INPUT_FILE_TMP_DIR = str(
        os.getenv("FRELATAGE_INPUT_FILE_TMP_DIR", "/tmp/frelatage")
    )

    # Maximum size of an input variable in bytes
    # Must be greater than 4
    if not 4 <= int(os.getenv("FRELATAGE_INPUT_MAX_LEN", 1024)) <= math.inf:
        raise FrelatageConfigError("FRELATAGE_INPUT_MAX_LEN must be greater than 4")
    FRELATAGE_INPUT_MAX_LEN = int(os.getenv("FRELATAGE_INPUT_MAX_LEN", 1024))

    # Maximum number of simultaneous threads
    # Must be greater than 8
    if not 8 <= int(os.getenv("FRELATAGE_MAX_THREADS", 20)) <= math.inf:
        raise FrelatageConfigError("FRELATAGE_MAX_THREADS must be greater than 8")
    FRELATAGE_MAX_THREADS = int(os.getenv("FRELATAGE_MAX_THREADS", 20))

    # Maximum number of stages for a fuzzed function
    # Must be in range greater than 1
    if not 1 <= int(os.getenv("FRELATAGE_MAX_STAGES", 1000000)) <= math.inf:
        raise FrelatageConfigError("FRELATAGE_MAX_STAGES must be greater than 1")
    FRELATAGE_MAX_STAGES = int(os.getenv("FRELATAGE_MAX_STAGES", 1000000))

    # Maximum number of successives cycle without a new path
    # Must be greater than 10
    if (
        not 10
        <= int(os.getenv("FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS", 5000))
        <= math.inf
    ):
        raise FrelatageConfigError(
            "FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS must be in range 10~10000"
        )
    FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS = int(
        os.getenv("FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS", 5000)
    )

    # Default directory for dictionaries
    # Relative path (to the path of the fuzzing file)
    FRELATAGE_DICTIONARY_DIR = str(
        os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            os.getenv("FRELATAGE_DICTIONARY_DIR", "./dict"),
        )
    )

    # Default directory for input files
    # Relative path (to the path of the fuzzing file)
    FRELATAGE_INPUT_DIR = str(
        os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            os.getenv("FRELATAGE_INPUT_DIR", "./in"),
        )
    )
