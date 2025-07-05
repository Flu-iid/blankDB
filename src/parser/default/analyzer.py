"""Basic Analyzer class for checking syntax and getting it ready for tokenizer"""

from string import whitespace


class Analyzer:
    """Checks lexicography rules (avoid_set)\
          and splits the syntax to sentences ready be tokenizer (sep_set)."""

    # lex rules
    AVOID_SET = set("1")
    SEP_SET = set(whitespace)
    END_SET = set(";")

    def __init__(
        self,
        user_input: str | None = None,
        sep: set | None = None,
        avoid: set | None = None,
        end: set | None = None,
    ) -> None:
        self.avoid = avoid if avoid else Analyzer.AVOID_SET
        self.sep = sep if sep else Analyzer.SEP_SET
        self.end = end if end else Analyzer.END_SET
        self.sentences: list[Sentence] | list = []
        self.status: bool = False
        self.result = self.analyze(user_input) if user_input else None

    def __repr__(self) -> str:
        return f"Alanyzer_object: {self.sentences}"

    def analyze(self, s: str) -> None:
        """check if everything is write according to lex rules (self.avoid)\
        also split the raw syntax and store in self.syntax_list.
        """
        pos = 0
        new_sentence = Sentence()
        for i, c in enumerate(s):
            try:
                if c in self.avoid:
                    raise SyntaxError

                elif c in self.end:
                    new_sentence.append(s[pos:i])
                    self.sentences.append(new_sentence)
                    pos = i + 1
                    new_sentence = Sentence()
                    # end of sentence

                elif i == len(s) - 1:
                    new_sentence.append(s[pos : i + 1])
                    self.sentences.append(new_sentence)
                    pos = i + 1
                    # end of syntax or input

                elif c in self.sep:
                    if pos != i:
                        new_sentence.append(s[pos:i])
                    pos = i + 1
                    # jump from seperator chars

            except SyntaxError:
                print(
                    f"Syntax Error: invalid syntax on {i}:{c}. check avoid_set\n\
AVOID_SET: {self.AVOID_SET}"
                )
                return self.status
        self.status = True
        return self.status


class Sentence:
    """Object presentation of sentence in a syntax. `[elements](len)`"""

    def __init__(self, data: list[str] | None = None) -> None:
        self._data = data if data else []

    def __repr__(self) -> str:
        return f"[{', '.join(self._data)}]({len(self._data)})"

    def append(self, e) -> None:
        self._data.append(e)

    def __len__(self) -> int:
        return len(self._data)

    def __inter__(self) -> None:
        return iter(self._data)

    def __getitem__(self, index) -> str:
        return self._data[index]

    def __setitem__(self, index, value) -> None:
        self._data[index] = value

    def __delitem__(self, index) -> None:
        del self._data[index]
