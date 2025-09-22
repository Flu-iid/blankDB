"""Constant modules holding sql rules for parser"""

from string import whitespace, digits, ascii_letters
from typing import Any

# analyzer rules

AVOID_SET: set[Any] = set()  # characters to avoid
SEP_SET: set[str] = set(whitespace)  # character seprating each word
# KEEP_SEP = False  # keep seperator as well
END_SET: set[str] = set(";")  # character ending each query

# token rules
TID_RULES: set[str] = set(ascii_letters + digits)
TINT_RULES: set[str] = set(digits)
TKW_RULES: set[str] = {  # needs better fix for 2kw together
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
