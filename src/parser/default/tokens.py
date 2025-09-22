from abc import ABC, abstractmethod
from typing import Any

from .errors import TokenTypeError
from . import TID_RULES, TINT_RULES, TKW_RULES


class Token(ABC):
    """object representation of tokens"""

    types: tuple = ()

    def __init__(self, token_type: str, token_value: str) -> None:
        self.__token_type: str = token_type
        self.__token_value: str = token_value
        if self.__class__ not in Token.types:
            Token.types += (self.__class__,)
        if not self.is_valid():
            raise TokenTypeError(f"Wrong value for {token_type}")

    @property
    def token_type(self) -> str:
        """token type property"""
        return self.__token_type

    @property
    def token_value(self) -> str:
        """token value property"""
        return self.__token_value

    @token_value.setter
    def token_value(self, new_token_value: Any) -> None:
        """set new token_value"""
        self.__token_value = new_token_value

    @abstractmethod
    def __repr__(self) -> str:
        """Token Representation"""

    @abstractmethod
    def is_valid(self) -> bool:
        """Token Validation"""


class Tid(Token):
    """object representaion of ID tokens"""

    RULES: set[str] = TID_RULES

    def __init__(self, token_value: str) -> None:
        super().__init__("ID", token_value)

    def __str__(self) -> str:
        return self.token_value

    def __repr__(self) -> str:
        return f"Tid({self.token_value})"

    def is_valid(self) -> bool:
        """Check if correct according to rules"""
        value_set: set[str] = set(self.token_value)
        if value_set <= Tid.RULES:
            return True
        return False


class Tint(Token):
    """object representaion of INT tokens"""

    RULES: set[str] = TINT_RULES

    def __init__(self, token_value: str) -> None:
        super().__init__("INT", token_value)

    def __int__(self) -> int:
        return int(self.token_value)

    def __repr__(self) -> str:
        return f"Tint({self.token_value})"

    def is_valid(self) -> bool:
        """Check if correct according to rules"""
        value_set: set[str] = set(self.token_value)
        if value_set <= Tint.RULES:
            return True
        return False


class Tkeyword(Token):
    """object representaion of KEYWORD tokens"""

    RULES: set[str] = TKW_RULES

    def __init__(self, token_value: str) -> None:
        super().__init__("KEYWORD", token_value)

    def __repr__(self) -> str:
        return f"Tkw({self.token_value})"

    def is_valid(self) -> bool:
        """Check if correct according to rules"""
        if self.__token_value.upper() in Tkeyword.RULES:
            return True
        return False
