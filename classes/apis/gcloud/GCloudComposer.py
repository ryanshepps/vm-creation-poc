from .classes.BootDisk import BootDisk
from .classes.Instance import Instance
from .classes.InstanceRequest import InstanceRequest
from .classes.Network import Network
from classes.abstractions.Composer import Composer
from classes.abstractions.Parser import Parser
from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.Logger import Logger

from google.cloud import compute_v1
import google.api_core.exceptions


class GCloudComposer(Composer):

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

        for instance_configuration in parsed_file:
            instance_boot_disk = BootDisk(instance_configuration)
            instance_network = Network()

            instance = Instance(
                instance_configuration,
                [instance_boot_disk],
                [instance_network])
            instance_request = InstanceRequest(
                instance_configuration,
                instance)

            self.logger.info(f'Creating Instance: \n{instance}')

            instance_client = compute_v1.InstancesClient()
            operation = instance_client.insert(request=instance_request)
            operation.result()  # Waits for operation to complete sychronously.

            self.logger.info(
                f'Successfully created {instance_configuration["name"]}')
            live_instance = instance_client.get(
                project=instance_configuration["project"],
                zone=instance_configuration["zone"],
                instance=instance_configuration["name"])
            self.logger.info(f'Live Instance: \n{live_instance}')
