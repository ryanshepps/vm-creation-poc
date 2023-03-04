from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.Logger import Logger


class AzureValidator(Validator):

    def __init__(self):
        super().__init__()
        self.logger = Logger(__name__)

    def validate(self, to_validate: dict) -> bool:
        for single_vm_config in to_validate:
            self.__validate_required_keys(single_vm_config)

        return True

    def __validate_required_keys(self, to_validate: dict):
        required_keys = [
            "name", "resource-group", "image", "location", "admin-username"]

        missing_keys = []
        for required_key in required_keys:
            if required_key not in to_validate:
                missing_keys.append(required_key)

        if len(missing_keys) != 0:
            raise InvalidConfigError(f"Required keys {str(missing_keys)} are \
missing.")
