from .ResourceGroup import ResourceGroup
from ....Logger import Logger

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class Network:

    def __init__(
            self, *, SubscriptionID: int, ResourceGroup: ResourceGroup,
            VM_Configuration: dict):
        self.logger = Logger(__name__)
        self.resource_group = ResourceGroup
        self.vm_configuration = VM_Configuration

        credentials = AzureCliCredential()
        self.network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        self.virtual_network_name = f"{VM_Configuration['name']}-vnet"
        self.subnet_name = f"{VM_Configuration['name']}-subnet"
        self.ip_configuration_name = f"{VM_Configuration['name']}-ip-config"
        self.network_interface_name = f"{VM_Configuration['name']}-network-interface"

        self.__provision_virtual_network()
        subnet = self.__provision_subnet()
        self.network_interface = self.__provision_network_interface(subnet)

    def get_network_interface(self):
        return self.network_interface

    def __provision_virtual_network(self):
        virtual_network_parameters = {
            "location": self.vm_configuration["location"],
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }

        self.logger.info(f"Provisioning Virtual Network for \
{self.vm_configuration['name']}: \n\
resource_group_name: {self.resource_group.name}\n\
virtual_network_name: {self.virtual_network_name}\n\
virtual_network_parameters: \n\
{Logger.dict_to_formatted_string(virtual_network_parameters, 1)}")

        virtual_network_poller = self.network_client.virtual_networks\
            .begin_create_or_update(
                self.resource_group.name,
                self.virtual_network_name,
                virtual_network_parameters,
            )

        return virtual_network_poller.result()

    def __provision_subnet(self):
        subnet_parameters = {
            "address_prefix": "10.0.0.0/24",
        }

        self.logger.info(f"Provisioning Subnet for \
{self.vm_configuration['name']}: \n\
resource_group_name: {self.resource_group.name}\n\
virtual_network_name: {self.virtual_network_name}\n\
subnet_name: {self.subnet_name}\n\
subnet_parameters: \n\
{Logger.dict_to_formatted_string(subnet_parameters, 1)}")

        subnet_poller = self.network_client.subnets.begin_create_or_update(
            self.resource_group.name,
            self.virtual_network_name,
            self.subnet_name,
            subnet_parameters
        )

        return subnet_poller.result()

    def __provision_network_interface(self, subnet):
        network_interface_parameters = {
            "location": self.vm_configuration["location"],
            "ip_configurations": [
                {
                    "name": self.ip_configuration_name,
                    "subnet": {
                        "id": subnet.id,
                    },
                }
            ]
        }

        self.logger.info(f"Provisioning Network Interface for \
{self.vm_configuration['name']}: \n\
resource_group_name: {self.resource_group.name}\n\
network_interface_name: {self.network_interface_name}\n\
network_interface_parameters: \n\
{Logger.dict_to_formatted_string(network_interface_parameters, 1)}")

        network_interface_poller = self.network_client.network_interfaces.begin_create_or_update(
            self.resource_group.name,
            self.network_interface_name,
            network_interface_parameters
        )

        return network_interface_poller.result()
