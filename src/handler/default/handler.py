from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.typing import Analyzer


"""Handler class"""

# get text display in terminal from view module


class Handler:
    """handle user commands as an object"""

    blankDB_repr = ["␢_db", "_␢", "␣db", "_DB"]

    def __init__(self, analyzer) -> None:
        self.user_input = ""
        self.exit_signal = False
        self.analyzer = analyzer()  # needs some error handling
        self.output = None

    def __repr__(self) -> str:
        """i: input value, e: exit signal value"""
        return f"Handler(i:{self.user_input})[e:{self.exit_signal}]"

    def get_input(self, prompt_repr: int = 0):
        """get user input.\ncan use prompt representation between:
        1: ␢_db
        2: _␢
        3: ␣db
        4: _DB
        """

        self.user_input = input(f"{Handler.blankDB_repr[prompt_repr]} > ")
        if self.user_input in ["!!", "exit"]:
            self.exit_signal = True

    def get_output(self):
        if not self.exit_signal:
            self.output = self.analyzer.analyze(self.user_input)
            return self.output
        else:
            return False, None

        # display result from view

    def logout(self):
        exit()
