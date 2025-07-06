"""main structure controling blankDB"""

from src.handler.default.handler import Handler
from src.parser.default.analyzer import Analyzer
from src.parser.default.tokenizer import Tokenizer


class BlankDB:
    """"""

    def __init__(self) -> None:
        self.handler = Handler()
        self.analyzer = Analyzer()
        self.tokenizer = Tokenizer()

    def cycle(self):
        self.handler.input()
        self.analyzer.analyze(self.handler.user_input)
        # add tokenizer
        # add parser

    def start(self):
        while not self.handler.exit_signal:
            self.cycle()
