import copy
import os
import sys
import random
from pathlib import Path
from typing import Type, Any
from frelatage.mutator.mutator import Mutator


def get_argument_size(argument, file: bool) -> int:
    """
    Return the argument size in bytes
    """
    if file:
        # File size
        size = os.path.getsize(argument)
    else:
        # Variable size in memory
        size = sys.getsizeof(argument)
    return size


def valid_mutators(self, input_type: Type, input_size: int) -> list[Mutator]:
    """
    Filters mutators by input type
    """
    # Argument type
    # e.g. "int", "str", "file"
    type_str = str(input_type.__name__) if input_type != "file" else "file"
    # Filtering mutators using the "allowed types" property of each mutator
    valid_mutators_type = list(
        filter(
            lambda mutator: type_str in mutator.allowed_types and mutator.enabled,
            self.mutators,
        )
    )

    # Prevents the input from increasing in size if the maximum allowed size has been reached
    max_input_size_reached = input_size > self.config.FRELATAGE_INPUT_MAX_LEN
    if max_input_size_reached:
        # Filtering mutators using the "size_effect" property of each mutator
        valid_mutators_size = list(
            filter(lambda mutator: "decrease" in mutator.size_effect, self.mutators)
        )
    else:
        valid_mutators_size = self.mutators

    # Filtered mutators
    valid_mutators = list(set(valid_mutators_type) & set(valid_mutators_size))
    return valid_mutators


def get_mutation(self, input: Any, file: bool) -> Any:
    """
    Generate a mutation in a recursive way for a variable
    e.g. : get_mutation(["a", 1, ["b"]])
            -> We start by mutating the global array
            -> Then we recursively mutate the elements of the array until
            all non-iterable elements have been reached. (In this particular
            case : "a", 1 and "b")
    """
    mutate = random.randint(0, 100) / 100 <= self.mutation_probability

    # If we mutate the input
    if mutate:
        input_type = type(input) if not file else "file"
        argument_size = get_argument_size(input, input_type == "file")

        valid_mutators = self.valid_mutators(input_type, argument_size)
        # # We use a random mutator among the valid ones
        mutator = random.choice(valid_mutators)
        # Root element mutation
        mutation = mutator.mutate(copy.deepcopy(input))

        is_list = isinstance(mutation, list)
        is_tuple = isinstance(mutation, tuple)
        is_iterable = is_list or is_tuple
        is_dict = isinstance(mutation, dict)

        # If the element is iterable we mutate all its children elements
        if is_iterable:
            # Convert the tuple into a list so that we can modify the elements
            mutation = list(mutation) if is_tuple else mutation
            for i in range(len(mutation)):
                valid_mutators = self.valid_mutators(type(mutation[i]), 1)
                mutation[i] = self.get_mutation(mutation[i], False)
            # Reconvert to a tuple
            mutation = tuple(mutation) if is_tuple else mutation

        elif is_dict:
            # Mutate keys
            for key in list(mutation.keys()):
                new_key = self.get_mutation(key, False)
                mutation[new_key] = mutation[key]
                del mutation[key]

            # Mutate values
            for key in mutation:
                valid_mutators = self.valid_mutators(type(mutation[key]), 1)
                mutation[key] = self.get_mutation(mutation[key], False)

    # If we don't mutate the input
    else:
        mutation = input
    return mutation


def generate_cycle_mutations(self, parents: list) -> list:
    """
    Generate a list of mutations with a list of parent mutations as an input
    """
    new_cycle = []

    # Mutation
    for thread in range(self.threads_count):

        # Selecting a random parent
        arguments = random.choice(parents)

        thread_arguments = []

        # We mutate each argument
        for argument in arguments:

            mutation = copy.deepcopy(argument)
            mutation.value = self.get_mutation(mutation.value, mutation.file)
            # Mutation of "file" type inputs
            if mutation.file:
                filename = os.path.split(mutation.value)[1]
                file_argument_id = os.path.split(os.path.split(mutation.value)[0])[1]
                base = Path(mutation.value).parents[2]
                new_argument = os.path.join(
                    base, str(thread), file_argument_id, filename
                )
                mutation.value = new_argument

            thread_arguments.append(mutation)
        new_cycle.append(thread_arguments)
    self.cycle = new_cycle
