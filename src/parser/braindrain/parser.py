"""simple parser for SQL syntaxes"""

from src.parser.classes_old import Tokenizer

AVOID_SET = {}


class Braindrain(Tokenizer):
    """"""

    def __init__(self) -> None:
        super().__init__()
        self.keywords
