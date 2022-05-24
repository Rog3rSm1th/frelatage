import contextlib
import os
import timeout_decorator
import trace
from typing import Callable, Iterable
from frelatage.config.config import Config
from frelatage.tracer.trace_result import Result


def supress_stdout(func: Callable):
    """
    redirect the output of a function to /dev/null
    """

    def wrapper(*a, **ka):
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stdout(devnull):
                return func(*a, **ka)

    return wrapper


class Tracer:
    """
    The tracer allows to launch a function and to keep track of the executed instructions
    as well as the triggered errors.
    """

    def __init__(
        self,
        exceptions_whitelist: Iterable[Exception] = [],
        exceptions_blacklist: Iterable[Exception] = [],
    ) -> None:
        """
        Initialize the tracer with an exception whitelist and an exception blacklist.
        """
        self.exceptions_whitelist = exceptions_whitelist
        self.exceptions_blacklist = exceptions_blacklist

    @timeout_decorator.timeout(
        Config.FRELATAGE_TIMEOUT_DELAY, use_signals=True, timeout_exception=TimeoutError
    )
    def runfunc(self, function: Callable, arguments):
        """
        Trace a function.
        The result will be stored in self.tracer.
        """
        self.tracer.runfunc(function, *arguments)

    @supress_stdout
    def trace(self, function: Callable, arguments: list) -> Result:
        """
        Trace a function and return a trace result object.
        """
        error = False
        error_type = None
        timeout = False

        # Initialize the tracer
        self.tracer = trace.Trace(ignoredirs=[], trace=0, count=1)

        arguments = [argument.value for argument in arguments]

        # Run the function and catch errors
        try:
            self.runfunc(function, arguments)
        # Whitelisted exceptions
        except self.exceptions_whitelist as e:
            error = True
            error_type = str(e.__class__.__name__)
        # Timeout exception
        except TimeoutError as e:
            timeout = True
            error_type = str(e.__class__.__name__)
        # Blacklisted exceptions
        except self.exceptions_blacklist as e:
            pass
        # Default exceptions
        except Exception as e:
            if self.exceptions_whitelist == ():
                error = True
                error_type = str(e.__class__.__name__)
            else:
                pass

        # List of the executed instructions
        instructions = list(self.tracer.results().counter.items())
        reached_instructions = [
            (instruction[0][0], instruction[0][1]) for instruction in instructions
        ]
        # List of the instructions pairs :
        # e.g : reached instructions : [('library.py', 1), ('library.py', 3), ('library.py', 2), ('library.py', 4)]
        #       instructions pairs -> [(('library.py', 3), ('library.py', 3)), (('library.py', 3), ('library.py', 2)), ...]
        instructions_pairs = []
        for i in range(len(reached_instructions)):
            instructions_pairs.append(
                (reached_instructions[i - 1], reached_instructions[i])
            )
        # Position of the instruction where the error occured, None if no error
        if error or timeout:
            error_position = (reached_instructions[-1], error_type)
        else:
            error_position = None

        # Generate a result object
        result = Result(
            error,
            error_type,
            timeout,
            error_position,
            reached_instructions,
            instructions_pairs,
        )
        return result
