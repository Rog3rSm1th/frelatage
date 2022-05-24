from typing import Any


class Report:
    def __init__(
        self,
        trace: Any,
        input: list,
        error: bool,
        timeout: bool,
        new_error_instruction: bool,
        reached_instructions_count: int,
        new_reached_instructions_count: int,
        instructions_pairs_count: int,
        new_instructions_pairs_count: int,
    ) -> None:
        """
        Report of the behavior of a function with given input
        """
        self.trace = trace
        self.input = input
        self.error = error
        self.timeout = timeout
        self.new_error_instruction = new_error_instruction
        self.reached_instructions_count = reached_instructions_count
        self.new_reached_instructions_count = new_reached_instructions_count
        self.instructions_pairs_count = instructions_pairs_count
        self.new_instructions_pairs_count = new_instructions_pairs_count

        self.score = self.compute_score()

    def compute_score(self) -> int:
        """
        The score of a report is used to select the most efficient inputs for the fuzzer's genetic algorithm mutations.
        The parameters are : the number of instructions reached, the number of new instructions reached, the number of
        pairs of instructions reached, the occurrence of an error/timeout.
        """

        result = (
            self.reached_instructions_count
            + self.new_reached_instructions_count
            + self.instructions_pairs_count
            + self.new_instructions_pairs_count
        )
        return result

    def __eq__(self, other):
        """
        Reports are sorted by score
        """
        return self.score == other.score

    def __lt__(self, other):
        """
        Reports are sorted by score
        """
        return self.score < other.score
