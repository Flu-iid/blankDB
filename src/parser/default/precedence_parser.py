"""default Precedence Parser module"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tokenizer import Token, Tkeyword, Tint, Tid
    from precedence_parser import Expression


class PParser:
    """Precedence Parser class. setting precedence to tokenized list execution."""

    def __init__(self) -> None:
        self.keywords = self.keywords | {"SELECT", "FROM", "CREATE"}


class Opitmizer:
    """Reorder expressions for logical and optimized execution"""

    def __init__(self) -> None:
        pass


class Expression:
    """Smallest logical element for precedence list.\n
    these are tokens mapped together as an expression ready
    to be mapped to right functionality"""

    def __init__(
        self,
        token_list: list[Token]
        | list[Token, Expression]
        | list[Expression]
        | list = [],
    ) -> None:
        self.input_list = token_list
        self.expression_list = []
        self.previous_item: Token | Expression | None = None
        self.lead: Token | Expression | None = None
        self.follow: Token | Expression | None = None

    def rule(self):
        """Check if syntax is right to be mapped"""
        for i, tk in enumerate(self.token_list):
            if isinstance(tk, Tkeyword):
                new_expression = Expression()
                new_expression.lead, new_expression = tk, self.token_list[i + 1]

    # def __init__(self, token_list: list) -> None:
    #     self.r_token_list = reversed(token_list)
    #     self.node_list = []  # objectified tokens

    # def node_maker(self) -> Token:
    #     """mapping tokens to the object from right to left (LR)"""
    #     new_node_list = []
    #     for i, token_repr in enumerate(self.r_token_list):
    #         token_type = token_repr[0]
    #         added_token = 0
    #         match token_type:
    #             case "ID":
    #                 added_token = Id(token_repr)
    #             case "INT":
    #                 added_token = Int(token_repr)
    #             case "KEYWORD":
    #                 previous_id_node: Token = new_node_list[i - 1]
    #                 added_token = Keyword(token_repr, previous_id_node)

    #         new_node_list.append(added_token)
    #     self.node_list += new_node_list
