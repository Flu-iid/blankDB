"""Basic Tokenizer Class"""

from string import ascii_letters, digits
from typing import Literal


class Tokenizer:
    """
    2. Tokenize: takes elements from Analyze part and maps to\
          the given tokenize values (if none were given, it uses default tokenize value)
    """

    default_tokens: dict[Literal["INT", "KEYWORD", "ID"], set[str]] = {
        "INT": set(digits),
        "KEYWORD": {  # needs better fix for 2kw together
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
        },
        "ID": {ascii_letters},
    }

    def __init__(self, tokens: dict | None = None) -> None:
        self.tokens = tokens if tokens else Tokenizer.default_tokens
        self.tokenized_list: list[list[Token]] | list = []
        self.status: bool = False
        self.result: tuple[bool, list[list[Token]]]

    def input_syntax_list(
        self, syntax_list: list[list[str]] | list | None = None
    ) -> None:
        self.syntax_list: list[list[str]] | list = syntax_list if syntax_list else []

    def tokenize(self) -> list:
        """map each element of syntax to the right token"""
        # using enumerate for easier debugging and error handling
        for si, syntax in enumerate(self.syntax_list):
            syntax_result: list = []
            cached_kw: Token | None = None
            for ei, element in enumerate(syntax):
                # check keywords
                if element.upper() in self.tokens["KEYWORD"]:
                    if cached_kw:
                        new_keyword: str = cached_kw.value + "_" + element.upper()
                        if new_keyword not in self.tokens["KEYWORD"]:
                            # raise error
                            pass
                        cached_kw = Tkeyword(new_keyword)
                    else:
                        cached_kw = Tkeyword(element.upper())
                else:
                    if cached_kw:
                        syntax_result.append(cached_kw)
                        cached_kw = None
                    if set(element) <= self.tokens["INT"]:
                        syntax_result.append(Tint(element))
                    else:
                        syntax_result.append(Tid(element))
            self.tokenized_list.append(syntax_result)
            # for now skipping operators

        # self.status = True
        # self.result = self.tokenized_list
        # return self.status, self.result
        return self.tokenized_list


class Token:
    """object representation of tokens"""

    def __init__(self, token_string: str) -> None:
        """unpack token_string values"""
        self.type = "RAW TOKEN"
        self.value: str = token_string

    def __repr__(self) -> str:
        return f"token: ({self.type, self.value})"


class Tid(Token):
    """object representaion of ID tokens"""

    RULES: set[str] = set(ascii_letters + digits)

    def __init__(self, token_string: str) -> None:
        super().__init__(token_string)
        self.type = "ID"

    def __str__(self) -> str:
        return self.value

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        value_set = set(self.value)
        if value_set <= self.RULES:
            return True
        return False


class Tint(Token):
    """object representaion of INT tokens"""

    RULES = set(digits)

    def __init__(self, token_string: str) -> None:
        self.rules: set[str] = Tint.RULES
        super().__init__(token_string)
        self.type = "INT"

    def __int__(self) -> int:
        return int(self.value)

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        value_set = set(self.value)
        if value_set <= self.RULES:
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

    def __init__(self, token_string: str) -> None:
        super().__init__(token_string)
        self.type = "KEYWORD"

    def is_correct(self) -> bool:
        """Check if correct according to rules"""
        if self.value.upper() in self.RULES:
            return True
        return False

    # def __repr__(self) -> str:
    #     # return f"KW: {self.value}, ID: {self.next.value}"
    #     return f"KW: {self.value}"


if __name__ == "__main__":
    Tid("sadad@@")
