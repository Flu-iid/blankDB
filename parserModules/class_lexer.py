"""default handy attributes and methodes for writing lexer/tokenizer"""

from string import whitespace, ascii_letters, digits


class Tokenizer:
    """A default tokenizer class
    it has 2 parts: Analyze and Tokenize.
    
    1. Analyze: checks lexicography rules (self.avoid_list)\
          and splits the syntax to elements ready be tokenized.

    2. Tokenize: takes elements from Analyze part and maps to\
          the given tokenize values (if none were given, it uses default tokenize value)
    """

    default_tokens = {
        "INT": set(digits),
        "KEYWORD": {"SELECT", "FROM"},
        "ID": {ascii_letters},
    }

    def __init__(self, token: dict | None = None, avoid: set | None = None) -> None:
        self.tokens = token if token else Tokenizer.default_tokens
        self.avoid = avoid if avoid else set()
        self.syntax_list: list[list[str]] | list = []
        self.tokenized_list: list[list[tuple[str, str]]] | list = []

    def analyze(self, s: str) -> None:
        """check if everything is write according to lex rules (self.avoid)\
        also split the raw syntax and store in self.syntax_list.
        """
        pos = 0
        result = []
        for i, c in enumerate(s):
            try:
                if c in self.avoid:
                    raise SyntaxError

                if i == len(s) - 1 or c == ";":
                    result.append(s[pos : i + 1])
                    self.syntax_list.append(result)
                    pos = i + 1
                    # end of syntax or input

                elif c in whitespace:
                    result.append(s[pos:i])
                    pos = i + 1

            except SyntaxError:
                print(f"Syntax Error: invalid syntax on {i}:{c}\n check avoid_list")
                return False
        return True

    def tokenize(self, lex_bool=True) -> None:
        """map each element of syntax to the right token"""
        if lex_bool:
            # using enumerate for easier debugging and error handling
            for si, syntax in enumerate(self.syntax_list):
                syntax_result = []
                for ei, element in enumerate(syntax):
                    # check keywords
                    if element.upper() in self.tokens["KEYWORD"]:
                        syntax_result.append(("KEYWORD", element.upper()))
                    elif set(element) <= self.tokens["INT"]:
                        syntax_result.append(("INT", element))
                    else:
                        syntax_result.append(("ID", element))
                self.tokenized_list.append(syntax_result)

                # for now skipping operators

    def input(self, s: str):
        """main function to get raw string syntax and get tokenized list\
            seperating each tokenized syntax as output"""
        correctness = self.analyze(s)
        self.tokenize(correctness)
        return self.tokenized_list
