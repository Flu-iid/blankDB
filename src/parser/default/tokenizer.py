"""Basic Tokenizer Class"""

from typing import Any, Optional
from .errors import SQLSyntaxError, TokenTypeError
from .tokens import Tkeyword, Tid, Tint, Token


class TokenGenerator:
    """Generating token based on raw value"""

    def __init__(self, value: None = None, second_value=Optional[str]) -> None:
        self._first_value = value

    @staticmethod
    def single_token_mapper(value: str) -> Tkeyword | Tint | Tid:
        """Single value to Token mapper"""
        if value.upper() in Tkeyword.RULES:
            return Tkeyword(value.upper())
        elif set(value) <= Tint.RULES:
            return Tint(value)
        elif set(value) <= Tid.RULES:
            if value[0] not in Tint.RULES:
                return Tid(value)
            else:
                raise SQLSyntaxError("Can't start ID value with digits")
        else:  # need more tokens to be handled
            raise SQLSyntaxError("Wrong syntax given")

    @staticmethod
    def double_token_mapper(left_val: Any, right_val: Any):
        """Double Token to Single Token Mapper"""
        if isinstance(left_val, Tkeyword) and isinstance(right_val, Tkeyword):
            return Tkeyword(f"{left_val.token_value}_{right_val.token_value}")
        # ...
        else:
            raise TokenTypeError("Unsupported Token Given")


class Tokenizer:
    """
    Tokenizer class\n
    Convert Analyzed List from Analyzer to Tokenized List
    """

    def __init__(self, analyzed_list: list[str]) -> None:
        self._analyzed_list: list[str] = analyzed_list  # use contextlib
        self._tokenized_list: list[Token] = []

    def tokenize(self):
        tg = TokenGenerator()
        for i, e in enumerate(self._analyzed_list):
            self._tokenized_list.append(tg.single_token_mapper(e))

        return self._tokenized_list


if __name__ == "__main__":
    pass
