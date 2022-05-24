import os
import time
import sys
import warnings
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import Callable, List
from frelatage.corpus.corpus import load_corpus
from frelatage.config.config import Config
from frelatage.mutator.mutator import *
from frelatage.queue.queue import Queue
from frelatage.tracer.tracer import Tracer

# Automatically retrieves the current version number
__version__ = version("frelatage")
__author__ = "Rog3rSm1th"
__email__ = "r0g3r5@protonmail.com"
__git__ = "https://github.com/Rog3rSm1th"
__twitter__ = "https://twitter.com/Rog3rSm1th"


class Fuzzer(object):
    """
    Copyright (c) 2022 Rog3rSm1th

    Frelatage is a coverage-based Python fuzzing library which can be used to fuzz python code.
    The development of Frelatage was inspired by various other fuzzers, including AFL/AFL++,
    Atheris and PyFuzzer.The main purpose of the project is to take advantage of the best features
    of these fuzzers and gather them together into a new tool in order to efficiently fuzz python applications.
    """

    from ._mutation import valid_mutators, get_mutation, generate_cycle_mutations
    from ._interface import (
        init_interface,
        refresh_interface,
        start_interface,
        exit_message,
    )
    from ._evaluate import evaluate_mutations
    from ._cycle import run_function, run_cycle
    from ._fuzz import fuzz
    from ._report import get_report_name, save_report
    from ._input import init_input_folder, init_file_input_arguments, init_file_inputs

    def __init__(
        self,
        method: Callable,
        corpus: list[object],
        threads_count: int = 8,
        exceptions_whitelist: list = (),
        exceptions_blacklist: list = (),
        output_directory: str = "./out",
        silent: bool = False,
    ) -> None:
        """
        Initialize the fuzzer
        """
        warnings.filterwarnings("ignore")

        # Frelatage configuration
        self.config = Config

        # Global set of reached instructions
        self.reached_instructions = set([])
        # Global set of instructions pairs
        self.instructions_pairs = set([])
        # Global set of instruction pairs executed during a crash
        self.favored_pairs = set([])
        # Global Set of positions where a crash occurred
        self.error_positions = set([])
        # Fuzzed method
        self.method = method

        # Remove duplicates in corpus
        corpus = [list(set(argument)) for argument in corpus]
        # Frelatage corpus
        self.corpus = corpus
        # List of all avalaibles mutators
        self.mutators = mutators
        # Number of concurrently launched threads
        self.threads_count = max(min(threads_count, Config.FRELATAGE_MAX_THREADS), 8)
        # List of cycle mutations
        self.cycle = []

        # Exceptions that will be taken into account or not when fuzzing
        self.exceptions_whitelist = exceptions_whitelist
        self.exceptions_blacklist = exceptions_blacklist

        # Frelatage tracer
        self.tracer = Tracer(
            exceptions_whitelist=self.exceptions_whitelist,
            exceptions_blacklist=self.exceptions_blacklist,
        )

        # Input and output directories
        # The working directory is the same as the fuzz file
        self.input_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])), Config.FRELATAGE_INPUT_DIR
        )
        self.output_directory = Path(
            os.path.join(
                os.path.dirname(os.path.realpath(sys.argv[0])), output_directory
            )
        ).as_posix()

        # Silent output
        self.silent = silent

        # Fuzzer statistics
        self.cycles_count = 0
        self.inputs_count = 0
        self.stage_inputs_count = 0
        self.unique_crashes = 0
        self.total_crashes = 0
        self.unique_timeout = 0
        self.total_timeouts = 0

        # Time statistics
        self.fuzz_start_time = datetime.now()
        self.last_new_path_time = None
        self.last_unique_crash_time = None
        self.last_unique_timeout_time = None

        # Genetic algorithm parameters
        self.survival_probability = 0.5
        self.mutation_probability = 0.3

        # Number of Frelatage cycles without finding new paths
        self.cycles_without_new_path = 0
        # Corpus entries that are still in the queue
        self.queue = Queue(self.corpus)
        # Current arguments
        self.arguments = self.queue.current_arguments()

        # Executions per second
        self.last_seconds_executions = 0
        self.executions_per_second = 0
        self.current_second = int(time.time())

        # Initialize file input folders in /tmp/frelatage (default value)
        # Can be modified using the FRELATAGE_INPUT_FILE_TMP_DIR env variable
        self.init_file_inputs()
