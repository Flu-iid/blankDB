"""simple parser for SQL syntaxes"""

from src.parser.classes import Tokenizer


class SQLTokenizer(Tokenizer):
    """"""

    def __init__(self) -> None:
        super().__init__()
        self.keywords = self.keywords | {"SELECT", "FROM", ";"}
