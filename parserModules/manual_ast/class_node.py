"""class holder for AST nodes"""


class Token:
    """object representation of token in ast"""

    def __init__(self, token_string: tuple) -> None:
        """unpack token_string values"""
        self.type, self.value = token_string
        self.next = None

    def __repr__(self) -> str:
        return f"token: {self.type, self.value}"


class Id(Token):
    """object representaion of ID tokens"""

    def __init__(self, token_string: tuple) -> None:
        super().__init__(token_string)

    def __str__(self) -> str:
        return self.value


class Int(Token):
    """object representaion of INT tokens"""

    def __init__(self, token_string: tuple) -> None:
        super().__init__(token_string)

    def __int__(self) -> int:
        return int(self.value)


class Keyword(Token):
    """object representaion of KEYWORD tokens"""

    def __init__(self, token_string: tuple, id: Id) -> None:
        super().__init__(token_string)
        self.next = id

    def __repr__(self) -> str:
        return f"KW: {self.value}, ID: {self.next.value}"


class Expression:
    """handling token_list and mapping to proper functions"""

    def __init__(self, token_list: list) -> None:
        self.r_token_list = reversed(token_list)
        self.node_list = []  # objectified tokens

    def node_maker(self) -> Token:
        """mapping tokens to the object from right to left (LR)"""
        new_node_list = []
        for i, token_repr in enumerate(self.token_list):
            token_type, token_value = token_repr
            added_token = 0
            match token_type:
                case "ID":
                    added_token = Id(token_value)
                case "INT":
                    added_token = Int(token_value)
                case "KEYWORD":
                    added_token = Keyword(token_value, new_node_list[i - 1])

            new_node_list.append(added_token)

        self.node_list += new_node_list

        # need to decide how to handle token objects in tree
