"""Error handling module"""


class TokenTypeError(Exception):
    """Token Type Error"""


class SQLSyntaxError(Exception):
    "SQL Syntax Error"


class LexicalError(Exception):
    """Used avoid char specifiec by parser"""
