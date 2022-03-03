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
    error_position: int
    # All groups of two successive instructions reached during the execution of a function
    # e.g : [(1, 2), (2, 5), (5, 6), (6, 3)]
    instructions_pairs: list
    # List of the reached instructions during the execution of a function
    reached_instructions: list[tuple]