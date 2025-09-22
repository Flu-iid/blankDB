from typing import TYPE_CHECKING
from default.tokens import Tid, Token

if TYPE_CHECKING:
    from src.parser.default.tokens import Tid, Token

t = Tid("aa1")

print(t.types)
