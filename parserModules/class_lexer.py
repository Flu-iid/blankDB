"""default handy attributes and methodes for writing lexer/tokenizer"""

from string import whitespace


class Tokenizer:
    """handy Tokenizer class function and values"""

    def __init__(self) -> None:
        self.keywords = set()
        self.avoid = set()
        self.syntax_list = []
        self.token_list = []

    def check_lex(self, s: str) -> bool:
        """check if everything is write according to lex rules (self.avoid)"""
        if s in self.avoid:
            return False
        return True

    def splitter(self, s: str) -> None:
        """split the syntax and store in self.syntax_list"""
        pos = 0
        result = []
        for i, c in enumerate(s):
            if i == len(s) - 1 or c == ";":
                self.syntax_list.append(result)
                result.clear()
                # end of syntax or input

            elif c in whitespace:
                pass

    def get_syntax(self, s: str) -> None:
        self.syntax.append(s)
        # also tokenize
