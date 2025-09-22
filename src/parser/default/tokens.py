from abc import ABC, abstractmethod
from string import ascii_letters, digits
from typing import Any, Optional

from .errors import SQLSyntaxError, TokenTypeError


class Token(ABC):
    """object representation of tokens"""

    types: tuple = ()

    def __init__(self, token_type: str, token_value: str) -> None:
        self.__token_type: str = token_type
        self.__token_value: str = token_value
        if self.__class__ not in Token.types:
            Token.types += (self.__class__,)
        if not self.is_correct():
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
    def is_correct(self) -> bool:
        """Token Validation"""


class Tid(Token):
    """object representaion of ID tokens"""

    RULES: set[str] = set(ascii_letters + digits)

    def __init__(self, token_value: str) -> None:
        super().__init__("ID", token_value)

    def __str__(self) -> str:
        return self.token_value

    def __repr__(self) -> str:
        return f"Tid({self.token_value})"

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        value_set: set[str] = set(self.token_value)
        if value_set <= Tid.RULES:
            return True
        return False


class Tint(Token):
    """object representaion of INT tokens"""

    RULES: set[str] = set(digits)

    def __init__(self, token_value: str) -> None:
        super().__init__("INT", token_value)

    def __int__(self) -> int:
        return int(self.token_value)

    def __repr__(self) -> str:
        return f"Tint({self.token_value})"

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        value_set: set[str] = set(self.token_value)
        if value_set <= Tint.RULES:
            return True
        return False


class Tkeyword(Token):
    """object representaion of KEYWORD tokens"""

    RULES: set[str] = {  # needs better fix for 2kw together
        "SELECT",
        "FROM",
        "CREATE",
        "TABLE",
        "CREATE_TABLE",
        "DROP",
        "DROP_TABLE",
        "INSERT",
        "INTO",
        "INSERT_INTO",
        "DELETE",
        "DELETE_FROM",
    }

    def __init__(self, token_value: str) -> None:
        super().__init__("KEYWORD", token_value)

    def __repr__(self) -> str:
        return f"Tkw({self.token_value})"

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        if self.__token_value.upper() in Tkeyword.RULES:
            return True
        return False


class TokenGenerator:
    """Generating token based on raw value"""

    def __init__(self, value: str, second_value=Optional[str]) -> None:
        self._first_value: str = value

    @staticmethod
    def single_token_mapper(value: str) -> Tkeyword | Tint | Tid:
        """Single value to Token mapper"""
        if value.upper() in Tkeyword.RULES:
            return Tkeyword(value.upper())
        elif set(value) <= Tint.RULES:
            return Tint(value)
        elif set(value) <= Tid.RULES:
            if value[0] not in digits:
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
