import datetime
import getpass

from .classes.Image import Image
from .classes.Network import Network
from .classes.ResourceGroup import ResourceGroup
from .classes.Subscription import Subscription
from .classes.VirtualMachine import VirtualMachine
from classes.abstractions.Composer import Composer
from classes.abstractions.Parser import Parser
from classes.abstractions.Validator import Validator
from classes.exceptions.InvalidConfigError import InvalidConfigError
from classes.VMDocumenter import VMDocumenter
from classes.Logger import Logger


class AzureComposer(Composer):

    def __init__(self, *, Parser: Parser, Validator: Validator) -> None:
        super().__init__(Parser=Parser, Validator=Validator)
        self.logger = Logger(__name__)

    def __request_admin_password(self, vm_name: str) -> str:
        return getpass.getpass(prompt=f"Admin password for {vm_name}: ")

    def compose_from_file(self, file_location: str) -> None:
        parsed_file = self.parser.parse(file_location)

        try:
            self.validator.validate(parsed_file)
        except InvalidConfigError as e:
            raise InvalidConfigError(f"{file_location} is invalid. {e}") from\
                None

        subscription_id = Subscription().subscription_id

        for vm_configuration in parsed_file:
            vm_configuration["admin-password"] = \
                self.__request_admin_password(vm_configuration["name"])
            vm_configuration["image-reference"] = Image(vm_configuration)

            vm_resouce_group = ResourceGroup(subscription_id, vm_configuration)
            vm_network = Network(
                SubscriptionID=subscription_id, ResourceGroup=vm_resouce_group,
                VM_Configuration=vm_configuration)
            vm = VirtualMachine(
                SubscriptionID=subscription_id, ResourceGroup=vm_resouce_group,
                Network=vm_network.get_network_interface(),
                VM_Configuration=vm_configuration)

            now = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
            vm_doc_file_name = f"docs/azure/vm/VMcreation_{now}.txt"
            vm_config_doc_file_name = f"docs/azure/vm_config/azure_{now}.conf"
            VMDocumenter().document(
                vm.result, vm_doc_file_name, file_location,
                vm_config_doc_file_name)
