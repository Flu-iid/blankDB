from string import ascii_letters, digits
from unicodedata import digit

from .analyzer import Analyzer


__all__: list[str] = ["Analyzer"]


TID_RULES = set(ascii_letters + digits)
TINT_RULES = set(digits)
TKW_RULES = {  # needs better fix for 2kw together
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
