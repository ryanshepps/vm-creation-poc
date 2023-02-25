from classes.abstractions.Validator import Validator
from classes.Logger import Logger


class GCloudValidator(Validator):

    def __init__(self):
        super().__init__()
        self.logger = Logger(__name__)

    def validate(self):
        pass
