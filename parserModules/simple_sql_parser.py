"""simple parser for SQL syntaxes"""

from string import whitespace
from class_lexer import Tokenizer


class SQLTokenizer(Tokenizer):
    """"""

    def __init__(self) -> None:
        super().__init__()
        self.keywords = self.keywords | {"SELECT", "FROM", ";"}
