from abc import ABC, abstractmethod


class Validator(ABC):

    @abstractmethod
    def validate(self, to_validate: dict) -> bool:
        pass
