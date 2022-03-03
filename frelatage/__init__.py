from frelatage.config.config import Config
from frelatage.tracer.tracer import Tracer
from frelatage.mutator.mutator import *
from frelatage.input.input import Input 
from typing import Type, Iterable, Callable, List
from datetime import datetime
import time
import sys
import os

class Fuzzer(object):
    """
    Copyright (c) 2022 Rog3rSm1th

    Frelatage is a coverage-based Python fuzzing library which can be used to fuzz python code. 
    The development of Frelatage was inspired by various other fuzzers, including AFL/AFL++, 
    Atheris and PyFuzzer.The main purpose of the project is to take advantage of the best features 
    of these fuzzers and gather them together into a new tool in order to efficiently fuzz python applications.
    """
    from ._mutation import valid_mutators, get_mutation, generate_cycle_mutations
    from ._interface import init_interface, refresh_interface, start_interface
    from ._evaluate import evaluate_mutations
    from ._cycle import run_function, run_cycle  
    from ._fuzz import fuzz
    from ._report import get_report_name, save_report
    from ._input import init_input_folder, init_file_input_arguments, init_file_inputs

    def __init__(self,
                 method: Callable,
                 arguments: list[object],
                 threads_count: int = 8,
                 exceptions_whitelist: list = (),
                 exceptions_blacklist: list = (),
                 output_directory: str = "./out",
                 input_directory: str = "./in"
        ) -> None:
        """
        Initialize the fuzzer
        """
        self.version = "0.0.1"
        
        # Frelatage configuration
        self.config = Config

        # Global set of reached instructions
        self.reached_instructions= set([])
        # Global set of instructions pairs
        self.instructions_pairs = set([])
        # Global set of instruction pairs executed during a crash
        self.favored_pairs = set([])
        # Global Set of positions where a crash occurred
        self.error_positions = set([])
        # Fuzzed method
        self.method = method

        # Initials function arguments
        self.arguments = arguments
        # List of all avalaibles mutators
        self.mutators = mutators
        # Number of concurrently launched threads
        self.threads_count = min(threads_count, Config.FRELATAGE_MAX_THREADS)
        # List of cycle mutations
        self.cycle = []

        # Exceptions that will be taken into account or not when fuzzing
        self.exceptions_whitelist = exceptions_whitelist
        self.exceptions_blacklist = exceptions_blacklist

        # Frelatage tracer
        self.tracer = Tracer(exceptions_whitelist=self.exceptions_whitelist, exceptions_blacklist=self.exceptions_blacklist)

        # Input and output directories
        # The working directory is the same as the fuzz file
        self.input_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            input_directory
        )
        self.output_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            output_directory
        )

        # Fuzzer statistics
        self.cycles_count = 0
        self.inputs_count = 0
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

        # Initialize file input folders in /tmp/frelatage (default value)
        # Can be modified using the FRELATAGE_INPUT_FILE_TMP_DIR env variable
        self.init_file_inputs()