"""Simple handler class"""

# get text display in terminal from view module


class Handler:
    """handle user commands"""

    def __init__(self, user_input: str = "") -> None:
        self.user_input = user_input
        self.exit_signal = False

    def __repr__(self) -> str:
        """i: input value, e: exit signal value"""
        return f"Handler(i:{self.user_input})[e:{self.exit_signal}]"

    def input(self):
        """get user input"""
        self.user_input = input("blankDB > ")
        if self.user_input in ["!!", "exit"]:
            self.exit_signal = True

    def output(self):
        pass
        # display result from view

    def logout(self):
        exit()
