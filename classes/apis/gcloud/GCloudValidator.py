import re

from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.Logger import Logger


class GCloudValidator(Validator):

    def __init__(self):
        super().__init__()
        self.logger = Logger(__name__)

    def validate(self, to_validate: dict) -> bool:
        for single_vm_config in to_validate:
            self.__validate_required_keys(single_vm_config)
            self.__validate_vm_name(single_vm_config)

        return True

    def __validate_required_keys(self, to_validate: dict):
        required_keys = ["name", "image", "imageproject", "zone"]

        missing_keys = []
        for required_key in required_keys:
            if required_key not in to_validate:
                missing_keys.append(required_key)

        if len(missing_keys) != 0:
            raise InvalidConfigError(f"Required keys {str(missing_keys)} are \
missing.")

    def __validate_vm_name(self, to_validate: dict):
        if not re.match("^[a-z0-9]*$", to_validate["name"]):
            raise InvalidConfigError(f"VM name {to_validate['name']} can only \
contain lowercase letters and numbers.")
