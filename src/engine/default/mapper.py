"""Mapping precedence list with right functionality"""

from typing import NoReturn

from src.engine.default.storage import _from, _select


def mapper(precedence_list: list, mapper_list: list = []) -> NoReturn:
    """mapping precedence_list and engine functions using match/case"""
    for i, pair in enumerate(precedence_list):
        pair_value = pair.lead.value
        match pair_value:
            case "FROM":
                mapper_list.append(_from)
            case "SELECT":
                mapper_list.append(_select)
            case _:
                # handle error
                pass
