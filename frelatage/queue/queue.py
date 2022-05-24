import copy
import numpy as np
from frelatage.input.input import Input


class Queue:
    """
    The queue contains the list of possible combinations of the corpus entries.
    """

    def __init__(self, corpus: list[list[Input]]):
        self.position = 0
        self.corpus = corpus
        self.arguments = self.generate_arguments()
        self.currents_arguments = self.current_arguments()

    def generate_arguments(self):
        """
        Return all possible combinations of inputs.
        Corpus : [  [Input_1, Input_2],  [Input_3, Input_4]  ]
        Arguments : [
                      [Input_1, Input_3],
                      [Input_1, Input_4],
                      [Input_2, Input_3],
                      [Input_2, Input_4],
                    ]
        """
        arguments_list = np.array(np.meshgrid(*self.corpus)).T.reshape(
            -1, len(self.corpus)
        )
        # Deepcopy each Input instance to avoid collisions
        for i in range(len(arguments_list)):
            arguments = arguments_list[i]
            for j in range(len(arguments)):
                arguments_list[i][j] = copy.deepcopy(arguments_list[i][j])

        arguments = [list(arguments) for arguments in arguments_list]
        return arguments

    def current_arguments(self) -> list[Input]:
        """
        Return the current arguments
        """
        return self.arguments[self.position]

    @property
    def end(self) -> bool:
        """
        Check if we have reached the end of the queue
        """
        return self.position >= len(self.arguments)
