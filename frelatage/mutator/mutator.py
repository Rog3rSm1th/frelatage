import copy
import random
from typing import Any, Type
from frelatage.config.config import Config
from frelatage.mutator.dictionary import load_dictionary
from frelatage.mutator.magicValues import MagicValues

# Array containing all the mutators
mutators = []

# Load dictionary from the dictionary files
dictionary_folder = Config().FRELATAGE_DICTIONARY_DIR
dictionary = load_dictionary(dictionary_folder)


class Mutator(object):
    # "str", "int", "list", "dict", "NoneType", "float"
    allowed_types = set([])
    # "none", "increase", "decrease"
    size_effect = []
    # Is the mutator used by the fuzzer
    # True by default
    enabled = True

    @staticmethod
    def random_int(max: int) -> int:
        """
        Return a random integer.
        """
        if max == 1 or max == 0:
            return 0
        return random.randint(0, max - 1)

    @staticmethod
    def random_magic_value(magic_values_set: list) -> Any:
        """
        Return a random value from a magic value array.
        """
        return random.choice(magic_values_set)

    def mutate(self, input: Any) -> Any:
        """
        Function to mutate a given resource into another one.
        @return: new resource, or None if this mutator is not appropriate.
        """
        raise NotImplementedError(
            "mutate not implemented in {}".format(self.__class__.__name__)
        )


def register_mutator(mutator: Type[Mutator]) -> bool:
    """
    Register a mutator into the global mutators array
    """
    mutators.append(mutator)
    return True


# String mutators
@register_mutator
class MutatorStringBitFlip(Mutator):
    allowed_types = set(["str"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) == 0:
            return input
        position = Mutator.random_int(len(input))
        replacement_character = chr(ord(input[position]) ^ (1 << Mutator.random_int(8)))
        mutation = input[0:position] + replacement_character + input[position + 1 :]
        return mutation


@register_mutator
class MutatorStringAddSubByte(Mutator):
    allowed_types = set(["str"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) == 0:
            return input
        position = Mutator.random_int(len(input))
        delta = Mutator.random_int(256)
        replacement_character = chr((ord(input[position]) + delta) % 256)
        mutation = input[0:position] + replacement_character + input[position + 1 :]
        return mutation


@register_mutator
class MutatorStringInsertCharacter(Mutator):
    allowed_types = set(["str"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) == 0:
            return input
        position = Mutator.random_int(len(input))
        character = chr(Mutator.random_int(256))
        mutation = input[0:position] + character + input[position:]
        return mutation


@register_mutator
class MutatorStringInsertDict(Mutator):
    allowed_types = set(["str"])
    size_effect = ["increase"]
    # Disable if the dictionary is empty or if the dictionary fuzzing is disabled
    enabled = True if (dictionary and Config.FRELATAGE_DICTIONARY_ENABLE) else False

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) == 0:
            return input
        position = Mutator.random_int(len(input))
        character = random.choice(dictionary)
        mutation = input[0:position] + character + input[position:]
        return mutation


@register_mutator
class MutatorStringDeleteCharacter(Mutator):
    allowed_types = set(["str"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) == 0:
            return input
        position = Mutator.random_int(len(input))
        mutation = input[: position - 1] + input[position]
        return mutation


@register_mutator
class MutatorStringSwapTwoChars(Mutator):
    allowed_types = set(["str"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) < 2:
            return input
        first_character_position = Mutator.random_int(len(input))
        second_character_position = Mutator.random_int(len(input))
        # The position of the second character must be different from the first
        while first_character_position == second_character_position:
            second_character_position = Mutator.random_int(len(input))

        mutation = list(input)
        mutation[first_character_position], mutation[second_character_position] = (
            mutation[second_character_position],
            mutation[first_character_position],
        )
        mutation = "".join(mutation)
        return mutation


@register_mutator
class MutatorStringDuplicateSubString(Mutator):
    allowed_types = set(["str"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) < 2:
            return input
        first_character_position = Mutator.random_int(len(input))
        second_character_position = random.randint(first_character_position, len(input))
        substring = input[first_character_position:second_character_position]

        substring_position = Mutator.random_int(len(input))
        mutation = input[:substring_position] + substring + input[substring_position:]
        return mutation


@register_mutator
class MutatorStringRepeatSubString(Mutator):
    allowed_types = set(["str"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) < 2:
            return input
        first_character_position = Mutator.random_int(len(input))
        second_character_position = random.randint(first_character_position, len(input))
        substring = input[first_character_position:second_character_position]
        mutation = (
            input[:second_character_position]
            + substring
            + input[second_character_position:]
        )
        return mutation


@register_mutator
class MutatorStringDeleteSubString(Mutator):
    allowed_types = set(["str"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: str) -> str:
        if len(input) < 2:
            return input
        first_character_position = Mutator.random_int(len(input))
        second_character_position = random.randint(first_character_position, len(input))

        mutation = input[:first_character_position] + input[second_character_position:]
        return mutation


@register_mutator
class MutatorIntMagicValue(Mutator):
    allowed_types = set(["int"])
    size_effect = ["none", "increase", "decrease"]

    @staticmethod
    def mutate(input: int) -> int:
        mutation = random.choice(MagicValues.UINT)
        return mutation


@register_mutator
class MutatorIntAddSub(Mutator):
    allowed_types = set(["int"])
    size_effect = ["none", "increase", "decrease"]

    @staticmethod
    def mutate(input: int) -> int:
        mutation = input
        mutation += random.randint(-1000, 1000)
        return mutation


# List mutators
@register_mutator
class MutatorListDuplicateElement(Mutator):
    allowed_types = set(["list"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: list) -> list:
        if len(input) == 0:
            return input

        mutation = input.copy()
        position = Mutator.random_int(len(mutation))
        element = random.choice(mutation)
        mutation.insert(position, element)
        return mutation


@register_mutator
class MutatorListInsertNone(Mutator):
    allowed_types = set(["list"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: list) -> list:
        mutation = input.copy()
        mutation.append(None)
        return mutation


@register_mutator
class MutatorListRemoveElement(Mutator):
    allowed_types = set(["list"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: list) -> list:
        if len(input) == 0:
            return input

        mutation = input.copy()
        element_position = Mutator.random_int(len(mutation))
        mutation.pop(element_position)
        return mutation


@register_mutator
class MutatorListShuffle(Mutator):
    allowed_types = set(["list"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: list) -> list:
        if len(input) == 0:
            return input

        mutation = input.copy()
        random.shuffle(mutation)
        return mutation


# Tuple mutators
@register_mutator
class MutatorTupleDuplicateElement(Mutator):
    allowed_types = set(["tuple"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: tuple) -> tuple:
        if len(input) == 0:
            return input

        mutation = list(input)
        position = Mutator.random_int(len(mutation))
        element = random.choice(mutation)
        mutation.insert(position, element)
        mutation = tuple(mutation)
        return mutation


@register_mutator
class MutatorTupleInsertNone(Mutator):
    allowed_types = set(["tuple"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: tuple) -> tuple:
        mutation = list(input)
        mutation.append(None)
        mutation = tuple(mutation)
        return mutation


@register_mutator
class MutatorTupleRemoveElement(Mutator):
    allowed_types = set(["tuple"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: tuple) -> tuple:
        if len(input) == 0:
            return input

        mutation = list(input)
        element_position = Mutator.random_int(len(mutation))
        mutation.pop(element_position)
        mutation = tuple(mutation)
        return mutation


@register_mutator
class MutatorTupleShuffle(Mutator):
    allowed_types = set(["tuple"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: tuple) -> tuple:
        if len(input) == 0:
            return input

        mutation = list(input)
        random.shuffle(mutation)
        mutation = tuple(mutation)
        return mutation


# None mutators
@register_mutator
class MutatorNone(Mutator):
    allowed_types = set(["NoneType"])
    size_effect = ["none", "increase", "decrease"]

    @staticmethod
    def mutate(input: None) -> Any:
        types = ["a", 0, [], {}, 1.0, ()]
        mutation = random.choice(types)
        return mutation


# File mutators
@register_mutator
class MutatorFileFlipBit(Mutator):
    allowed_types = set(["file"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) == 0:
                return input
            else:
                position = Mutator.random_int(len(file_content))

                mutation = bytearray(file_content)
                mutation[position] = mutation[position] ^ (1 << Mutator.random_int(8))
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileInsertByte(Mutator):
    allowed_types = set(["file"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()

            mutation = bytearray(file_content)
            if len(file_content) == 0:
                mutation = chr(Mutator.random_int(256)).encode()
            else:
                position = Mutator.random_int(len(file_content))
                mutation = (
                    mutation[0:position]
                    + chr(Mutator.random_int(256)).encode()
                    + mutation[position:]
                )
            mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileDeleteByte(Mutator):
    allowed_types = set(["file"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) <= 2:
                return input
            else:
                position = Mutator.random_int(len(file_content))

                mutation = bytearray(file_content)
                mutation = mutation[0:position] + mutation[position + 1 :]
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileSwapTwoBytes(Mutator):
    allowed_types = set(["file"])
    size_effect = ["none"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) <= 2:
                return input
            else:
                first_byte_position = Mutator.random_int(len(file_content))
                second_byte_position = Mutator.random_int(len(file_content))
                # The position of the second character must be different from the first
                while first_byte_position == second_byte_position:
                    second_byte_position = Mutator.random_int(len(file_content))

                mutation = bytearray(file_content)
                mutation[first_byte_position], mutation[second_byte_position] = (
                    mutation[second_byte_position],
                    mutation[first_byte_position],
                )
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileDuplicateSubBytes(Mutator):
    allowed_types = set(["file"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) == 0:
                return input
            else:
                first_byte_position = Mutator.random_int(len(file_content))
                second_byte_position = random.randint(
                    first_byte_position, len(file_content)
                )
                mutation = bytearray(file_content)

                subbytes = mutation[first_byte_position:second_byte_position]
                subbytes_position = Mutator.random_int(len(file_content))
                mutation = (
                    mutation[:subbytes_position]
                    + subbytes
                    + mutation[subbytes_position:]
                )
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileRepeatSubBytes(Mutator):
    allowed_types = set(["file"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) == 0:
                return input
            else:
                first_byte_position = Mutator.random_int(len(file_content))
                second_byte_position = random.randint(
                    first_byte_position, len(file_content)
                )
                mutation = bytearray(file_content)

                subbytes = mutation[first_byte_position:second_byte_position]
                mutation = (
                    mutation[:second_byte_position]
                    + subbytes
                    + mutation[second_byte_position:]
                )
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileDeleteSubBytes(Mutator):
    allowed_types = set(["file"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()
            if len(file_content) <= 2:
                return input
            else:
                first_byte_position = Mutator.random_int(len(file_content))
                second_byte_position = random.randint(
                    first_byte_position, len(file_content)
                )
                mutation = bytearray(file_content)
                mutation = (
                    mutation[:first_byte_position] + mutation[second_byte_position:]
                )
                mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


@register_mutator
class MutatorFileInsertDict(Mutator):
    allowed_types = set(["file"])
    size_effect = ["increase"]
    # Disable if the dictionary is empty or if the dictionary fuzzing is disabled
    enabled = True if (dictionary and Config.FRELATAGE_DICTIONARY_ENABLE) else False

    @staticmethod
    def mutate(input: str) -> str:
        with open(input, "rb") as f:
            file_content = f.read()

            element = random.choice(dictionary)

            mutation = bytearray(file_content)
            if len(file_content) == 0:
                mutation = element.encode()
            else:
                position = Mutator.random_int(len(file_content))
                mutation = mutation[0:position] + element.encode() + mutation[position:]
            mutation = bytes(mutation)
        with open(input, "wb") as f:
            f.write(mutation)
        return input


# Dictionnary mutators
@register_mutator
class MutatorDictAddEntryInt(Mutator):
    allowed_types = set(["dict"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: dict) -> dict:
        mutation = copy.deepcopy(input)
        integer = random.choice(MagicValues.UINT)
        mutation[integer] = None
        return mutation


@register_mutator
class MutatorDictAddEntryString(Mutator):
    allowed_types = set(["dict"])
    size_effect = ["increase"]

    @staticmethod
    def mutate(input: dict) -> dict:
        mutation = input.copy()
        string = chr(Mutator.random_int(256))
        mutation[string] = None
        return mutation


@register_mutator
class MutatorDictDeleteEntry(Mutator):
    allowed_types = set(["dict"])
    size_effect = ["decrease"]

    @staticmethod
    def mutate(input: dict) -> dict:
        if len(input) == 0:
            return input
        mutation = input.copy()
        del mutation[random.choice(list(mutation.keys()))]
        return mutation


# Float mutators
@register_mutator
class MutatorFloatAddSub(Mutator):
    allowed_types = set(["float"])
    size_effect = ["none", "increase", "decrease"]

    @staticmethod
    def mutate(input: float) -> float:
        digits = Mutator.random_int(10)
        delta = random.uniform(-1000, 1000)
        mutation = round(input + delta, digits)
        return mutation
