from dataclasses import dataclass


@dataclass
class Result:
    """
    Result of a trace
    """

    # True if an error occurred during the execution of a function, false otherwise
    error: bool
    # Error type, e.g TypeError, ZeroDivisionError...
    error_type: str
    # True if an TimeOutError occurred during the execution of a function, false otherwise
    timeout: bool
    # Position of the instruction where the error occured
    error_position: tuple
    # All groups of two successive instructions reached during the execution of a function
    # e.g : [(('library.py', 3), ('library.py', 3)), (('library.py', 3), ('library.py', 2)), ...]
    instructions_pairs: list
    # List of the reached instructions during the execution of a function
    # e.g : [('library.py', 1), ('library.py', 3), ('library.py', 2), ('library.py', 4)]
    reached_instructions: list[tuple]
