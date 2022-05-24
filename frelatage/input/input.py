class Input:
    """
    Input can be either a file or any other type
    """

    def __init__(self, value: str = "", file: bool = False) -> None:
        self.value = value
        self.file = file

    def __iter__(self) -> None:
        yield "value", self.value
        yield "file", self.file
