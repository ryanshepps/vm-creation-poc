from classes.abstractions.Parser import Parser
from classes.Logger import Logger


class Parser(Parser):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)

    def parse(self, file_location: str) -> dict:
        pass
