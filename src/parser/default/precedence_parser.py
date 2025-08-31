"""default simple logic Precedence Parser module"""

from typing import TYPE_CHECKING, Any
from src.typing import Token, Tkeyword, Tint, Tid
from src.parser.default.tokenizer import Tokenizer

if TYPE_CHECKING:
    from src.typing import Token, Tkeyword, Tint, Tid
    # from src.typing import Pair


def pair_maker(token_list: list[Token]) -> list[Any]:
    """making Pair objects from token list"""
    result: list[Pair] = []
    last_index: int = len(token_list) - 1
    new_pair = None
    for i, e in enumerate(token_list):
        if i == 0 and not isinstance(e, Tkeyword):
            # handle error
            return

        if i == last_index:
            result.append(new_pair)

        if isinstance(e, Tkeyword):
            if i != 0:
                result.append(new_pair)
            new_pair = Pair()
            new_pair.lead = e

        elif isinstance(e, Tid):
            new_pair.tail.append(e)

        else:
            # handle error
            return

    return result


KEYWORD_LIST = Tokenizer.default_tokens["KEYWORD"]
KEYWORD_ORDER = {"FROM": 0, "SELECT": 1}


def pair_sort(pair_list: list) -> list:
    return sorted(pair_list, key=lambda a: KEYWORD_ORDER[a.lead.value])


class Pair:
    """Simple class to pair KeyWords and IDs.\n
    it has 2 attributes:\n
    1. lead: the first KW defining logic\n
    2. tail: the ID look up value for the logic."""

    def __init__(self) -> None:
        self.lead: Tkeyword | None = None
        self.tail: list[Token] | list = []

    def __repr__(self) -> str:
        return f"(lead:{self.lead}, tail:{self.tail})"
