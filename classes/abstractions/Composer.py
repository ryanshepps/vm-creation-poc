from abc import ABC, abstractmethod
from .Parser import Parser
from .Validator import Validator


class Composer(ABC):

    def __init__(self, *, Parser: Parser, Validator: Validator) -> None:
        self.parser = Parser
        self.validator = Validator

    @abstractmethod
    def compose_from_file(self, file_location: str) -> None:
        pass
