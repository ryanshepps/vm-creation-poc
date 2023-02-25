from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def parse(self, file_location: str) -> dict:
        pass
