"""Simple handler class"""

from ...parser.default.analyzer import Analyzer


class Handler:
    """handle user commands"""

    def __init__(self, user_input: str = "") -> None:
        self.user_input = user_input
        self.defualt_analyzer = Analyzer()
        self.result = self.defualt_analyzer.analyze(user_input)
        self.status = self.defualt_analyzer.status

    def __repr__(self) -> str:
        return "default Handler Object"

    def start(self):
        while True:
            print("blankDB> ", end="")
            self.user_input = input()
            if self.user_input in ["!!", "exit"]:
                self.logout()

            if not self.status:
                print(f"user input: {self.user_input}")

            # display result from view

    def logout(self):
        exit()
