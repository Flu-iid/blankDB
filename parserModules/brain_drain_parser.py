"""brain drain focuses on simplifying sql keywords and using signs instead. \
but it can take some time to get used to."""

from string import whitespace
import re


class BDTokenizer:
    """"""

    def __init__(self, syntax: str) -> None:
        self.syntax = syntax
        self.keywords = {"$", "@"}
        # $ ::= SELECT
        # @ ::= FROM
        self.avoid = {"."}
        self.token_list = []
        self.result = []

    def check_lex(self, s: str) -> bool:
        """"""
        if re.search(r"".join(self.avoid | self.keywords), s):
            return False
        return True

    def splitter(self, s: str) -> list[str]:
        """"""
        return s.translate(str.maketrans(whitespace, "." * 6))
        # whitespace module has 6 char

    def tokenizer(self, s:str) -> tuple[str, str]:
        """"""
        match = re.match(
            s,
            r"[a-zA-Z_][a-zA-Z0-9_]*"
            # add keywords ro regex as well
        )
        if match:
            raw_token = match.group()
            if raw_token == 


if __name__ == "__main__":
    o = SQLTokenizer("dgsgf")
    # print(o.check_lex("1"))
    s = re.search(r"".join(o.avoid | o.keywords), "1$")
    print(s)
