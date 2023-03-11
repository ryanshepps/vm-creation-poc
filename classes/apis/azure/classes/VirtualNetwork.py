from ....Logger import Logger
from .ResourceGroup import ResourceGroup

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class VirtualNetwork:

    def __new__(
            cls, *, SubscriptionID: str, ResourceGroup: ResourceGroup,
            VMConfiguration: dict):
        logger = Logger(__name__)

        credentials = AzureCliCredential()
        network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        virtual_network_name = f"{VMConfiguration['name']}-vnet"
        virtual_network_parameters = {
            "location": VMConfiguration["location"],
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }

        logger.info(f"Provisioning Virtual Network for \
{VMConfiguration['name']}: \n\
resource_group_name: {ResourceGroup.name}\n\
virtual_network_name: {virtual_network_name}\n\
virtual_network_parameters: \n\
{Logger.dict_to_formatted_string(virtual_network_parameters, 1)}")

        virtual_network_poller = network_client.virtual_networks\
            .begin_create_or_update(
                ResourceGroup.name,
                virtual_network_name,
                virtual_network_parameters,
            )

        return virtual_network_poller.result()
