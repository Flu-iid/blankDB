"""blankDB engine"""

from src.engine.default.mapper import mapper
from src.engine.default.storage import _from, _select


class SQLengine:
    """simple database engine class.\n
    read precedence list by mapper, and maps to correct functions of storage module."""

    def __init__(self, precedence_list) -> None:
        self._precedence_list: list = precedence_list
        self._mapped_list: list = []
        self.mapper()
        self._memory: list = [None] * len(self._mapped_list)
        self.process()

    def mapper(self) -> None:
        mapper(precedence_list=self._precedence_list, mapper_list=self._mapped_list)

    def process(self):
        for i, e in enumerate(self._precedence_list):
            match e.lead.value:
                case "FROM":
                    table_name = self._precedence_list[i].tail[0]
                    self._memory[i] = _from(table_name)
                case "SELECT":
                    table_path = self._memory[i - 1]
                    value = self._precedence_list[i].tail[0]
                    self._memory[i] = _select(value=value, table_path=table_path)

    # match case with Callable didnt work, have to work on it

    def result(self):
        return self._memory[-1]
