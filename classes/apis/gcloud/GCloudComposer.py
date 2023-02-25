from classes.abstractions.Composer import Composer
from classes.abstractions.Parser import Parser
from classes.abstractions.Validator import Validator
from classes.Logger import Logger


class GCloudComposer(Composer):

    def __init__(self, *, Parser: Parser, Validator: Validator) -> None:
        super().__init__(Parser=Parser, Validator=Validator)
        self.logger = Logger(__name__)

    def compose_from_file(self, file_location: str) -> None:
        pass
