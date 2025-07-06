"""simple parser for SQL syntaxes"""

from src.parser.classes import Tokenizer


class SQLTokenizer(Tokenizer):
    """"""

    def __init__(self) -> None:
        super().__init__()
        self.keywords = self.keywords | {"SELECT", "FROM", ";"}


class Expression:
    """tokens mapped together as an expression ready to be"""

    def __init__(self, token_list: list) -> None:
        self.r_token_list = reversed(token_list)
        self.node_list = []  # objectified tokens

    def node_maker(self) -> Token:
        """mapping tokens to the object from right to left (LR)"""
        new_node_list = []
        for i, token_repr in enumerate(self.r_token_list):
            token_type = token_repr[0]
            added_token = 0
            match token_type:
                case "ID":
                    added_token = Id(token_repr)
                case "INT":
                    added_token = Int(token_repr)
                case "KEYWORD":
                    previous_id_node: Token = new_node_list[i - 1]
                    added_token = Keyword(token_repr, previous_id_node)

            new_node_list.append(added_token)
        self.node_list += new_node_list
