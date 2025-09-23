"""analyzer module, for Handler's query_handler"""

from typing import Iterator, Optional, Any
from abc import ABC, abstractmethod

from .errors import LexicalError
from .SQL_RULES import AVOID_SET, END_SET, SEP_SET, SYNTAX_LANG


class QueryBase(ABC):
    """Base class for Query data and metadata"""

    lang: str = SYNTAX_LANG

    def __init__(self, input_object: Optional[Iterator[str] | str] = None) -> None:
        self.rule: str
        self.__query_lang: str = QueryBase.lang
        self.__base_list: list[str] = []
        if input_object:
            self._input_modifier(input_object)

    @property
    def base_list(self) -> list[Any]:
        """Query Base Type Property"""
        return self.__base_list

    @property
    def query_lang(self) -> str:
        """Query Syntax Language Property"""
        return self.__query_lang

    def _split(self, input_string: str) -> None:
        """split according to sql rules SEP_SET"""
        c_list: list[str] = []
        single_sep: str = self.rule[0]
        for c in input_string + single_sep:
            if c not in self.rule:
                c_list.append(c)
                continue
            self.base_list.append("".join(c_list))
            c_list.clear()

    def _input_modifier(self, input_object: Any) -> None:
        if isinstance(input_object, Iterator):  # input is iterator
            self.__base_list += list(input_object)
        elif isinstance(input_object, str):  # input is string
            self._split(input_object.strip(self.rule))
        # else  append manually

    @abstractmethod
    def append(self, new_object: Any) -> None:
        """Append new query word to BaseQuery"""
        ...

    def __len__(self) -> int:
        return len(self.base_list)

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __iter__(self) -> Iterator[Any]: ...

    @abstractmethod
    def __getitem__(self, index) -> Any: ...


class Query(QueryBase):
    """
    Query Class\n
    splitting and checking basic lexical rules for each query.
    """

    sep: str = SEP_SET

    def __init__(self, input_object: Optional[Iterator[str] | str] = None) -> None:
        self.rule = Query.sep
        super().__init__(input_object=input_object)
        self.__query_splitted: list[str] = self.base_list

    @property
    def query_splitted(self) -> list[str]:
        """Query Property"""
        return self.__query_splitted

    def append(self, query_word: str) -> None:
        """Append new query word to Query"""
        self.query_splitted.append(query_word)

    def __repr__(self) -> str:
        return f"[{', '.join(self.query_splitted)}]({len(self)})"

    def __iter__(self) -> Iterator[str]:
        return iter(self.query_splitted)

    def __getitem__(self, index) -> str:
        return self.query_splitted[index]


class QueryBatch(QueryBase):
    """
    Class Query List\n
    splitting each query according to sql rules END_SET
    """

    end: str = END_SET

    def __init__(self, input_object: Optional[Iterator[str] | str] = None) -> None:
        self.rule = QueryBatch.end
        super().__init__(input_object=input_object)
        self.__batch: list[Query] = self.base_list

    @property
    def batch(self) -> list[Query]:
        """Query Batch Property"""
        return self.__batch

    def append(self, new_query: Query) -> None:
        """Append new Query to QueryBatch"""
        self.batch.append(new_query)

    def __repr__(self) -> str:
        return f"QueryList:({len(self)} {'Queries' if len(self) > 1 else 'Query'})"

    def __iter__(self) -> Iterator[Query]:
        return iter(self.batch)

    def __getitem__(self, index) -> Query:
        return self.batch[index]


class SQL_Analyzer:
    """
    SQL Analyzer Class\n
    objectives:\n
    - check Lex rules according to SQL_RULES Constant\n
    - Initiate Query and QueryBatch Objects for Handler\n
    """

    avoid: str = AVOID_SET
    end: str = END_SET
    sep: str = SEP_SET

    def __init__(self) -> None:
        self.__input_string: str

    @property
    def input_string(self) -> str:
        """Input string property"""
        return self.__input_string

    @input_string.setter
    def input_string(self, new_string: str) -> None:
        self.__input_string = new_string

    def get_input(self, input_string) -> None:
        """Get new string value"""
        self.input_string = input_string

    def analyze(self, input_string: Optional[str] = None) -> QueryBatch:
        """
        Analyze Constructed object\n
        will return None if lexical rules arent considered according to AVOID_SET.
        """
        if input_string:
            self.input_string = input_string

        new_query = Query()
        batch = QueryBatch()
        pos: int = 0

        for i, c in enumerate(self.input_string.strip()):
            if c in SQL_Analyzer.avoid:
                raise LexicalError("Used avoid char specifiec by parser")
            elif c in SQL_Analyzer.end:
                new_query.append(self.input_string[pos:i])
                batch.append(new_query)
                pos = i + 1
                new_query = Query()
                # end of sentence
            elif i == len(self.input_string) - 1:
                new_query.append(self.input_string[pos : i + 1])
                batch.append(new_query)
                pos = i + 1
                # end of syntax or input
            elif c in SQL_Analyzer.sep:
                if pos != i:
                    new_query.append(self.input_string[pos:i])
                pos = i + 1
                # jump from seperator chars

        self.status = True
        return batch
