import datetime

from .classes.BootDisk import BootDisk
from .classes.Firewall import Firewall
from .classes.Instance import Instance
from .classes.InstanceRequest import InstanceRequest
from .classes.Network import Network
from classes.abstractions.Composer import Composer
from classes.abstractions.Parser import Parser
from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.VMDocumenter import VMDocumenter
from classes.Logger import Logger

from google.cloud import compute_v1
import google.auth


class GCloudComposer(Composer):

    def __init__(self, *, Parser: Parser, Validator: Validator) -> None:
        super().__init__(Parser=Parser, Validator=Validator)
        self.logger = Logger(__name__)

    def __get_project_id(self, instance_configuration):
        project_id = None

        if "project" in instance_configuration:
            project_id = instance_configuration["project"]
        else:
            self.logger.info(
                f"Project ID for {instance_configuration['name']} does not \
exist in configuration. Attempting to use project in GCloud CLI configuration.")
            _, project_id = google.auth.default()

        if project_id is None:
            raise InvalidConfigError(
                f"Could not find project ID for \
{instance_configuration['name']}. Consider setting the project in the \
instance configuration or set a default project via the GCloud CLI.")

        return project_id

    def compose_from_file(self, file_location: str) -> None:
        parsed_file = self.parser.parse(file_location)

        try:
            self.validator.validate(parsed_file)
        except InvalidConfigError as e:
            raise InvalidConfigError(f"{file_location} is invalid. {e}") from\
                None

        for instance_configuration in parsed_file:
            instance_configuration["project"] = self.__get_project_id(instance_configuration)

            instance_boot_disk = BootDisk(instance_configuration)
            instance_network = Network()
            if "ports" in instance_configuration:
                Firewall(
                    instance_network, instance_configuration)

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

            now = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
            vm_doc_file_name = f"docs/gcloud/vm/VMcreation_{now}.txt"
            vm_config_doc_file_name = f"docs/gcloud/vm_config/gcp_{now}.conf"
            VMDocumenter().document(
                live_instance, vm_doc_file_name, file_location,
                vm_config_doc_file_name)
