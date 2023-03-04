
from classes.abstractions.Composer import Composer
from classes.abstractions.Parser import Parser
from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.Logger import Logger


class AzureComposer(Composer):

    def __init__(self, *, Parser: Parser, Validator: Validator) -> None:
        super().__init__(Parser=Parser, Validator=Validator)
        self.logger = Logger(__name__)

    def compose_from_file(self, file_location: str) -> None:
        parsed_file = self.parser.parse(file_location)

        try:
            self.validator.validate(parsed_file)
        except InvalidConfigError as e:
            raise InvalidConfigError(f"{file_location} is invalid. {e}") from\
                None
