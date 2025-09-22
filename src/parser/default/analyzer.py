"""analyzer module, for Handler's query_handler"""

from typing import Iterator

from .errors import LexicalError
from .SQL_RULES import AVOID_SET, END_SET, SEP_SET


class Query:
    """
    Query Class\n
    splitting and checking basic lexical rules for each query.
    """

    sep: str = SEP_SET

    def __init__(self, raw_syntax: str) -> None:
        self.__query_words: list[str] = []
        self._split(raw_syntax.strip(Query.sep))

    @property
    def query_words(self) -> list[str]:
        """Query Type Property"""
        return self.__query_words

    def _split(self, input_string: str) -> None:
        """split according to sql rules SEP_SET"""
        c_list: list[str] = []
        single_sep: str = Query.sep[0]
        for c in input_string + single_sep:
            if c not in Query.sep:
                c_list.append(c)
                continue
            self.query_words.append("".join(c_list))
            c_list.clear()

    def __len__(self) -> int:
        return len(self.query_words)

    def __repr__(self) -> str:
        return f"[{', '.join(self.query_words)}]({len(self)})"

    def __iter__(self) -> Iterator[str]:
        return iter(self.query_words)

    def __getitem__(self, index) -> str:
        return self.query_words[index]


class QueryList:
    """
    Class Query List\n
    splitting each query according to sql rules END_SET
    """

    end: str = END_SET

    def __init__(self, raw_string: str) -> None:
        self.__query_list: list[Query] = []
        self._split(raw_string.strip(QueryList.end))

    @property
    def query_list(self) -> list[Query]:
        """Query List Property"""
        return self.__query_list

    def _split(self, input_string: str) -> None:
        """split according to sql rules END_SET"""
        c_list: list[str] = []
        single_end: str = QueryList.end
        for c in input_string + single_end:
            if c not in QueryList.end:
                c_list.append(c)
                continue
            syntax: str = "".join(c_list)
            query = Query(syntax)
            self.query_list.append(query)
            c_list.clear()

    def __len__(self) -> int:
        return len(self.query_list)

    def __repr__(self) -> str:
        return f"QueryList:({len(self)} {'Queries' if len(self) > 1 else 'Query'})"

    def __iter__(self) -> Iterator[Query]:
        return iter(self.query_list)

    def __getitem__(self, index) -> Query:
        return self.query_list[index]


class SQL_Analyzer:
    """
    SQL Analyzer Class
    """

    avoid: str = AVOID_SET

    def __init__(self) -> None:
        self.input_string: str

    def _is_valid(self) -> bool:
        for c in self.input_string:
            if c in SQL_Analyzer.avoid:
                return False
        return True

    def analyze(self, input_string: str) -> QueryList:
        """
        Analyze Constructed object\n
        will return None if lexical rules arent considered according to AVOID_SET.
        """
        self.input_string = input_string
        if self._is_valid():
            return QueryList(self.input_string)
        else:
            raise LexicalError("Used avoid char specified by parser in AVOID_SET")
