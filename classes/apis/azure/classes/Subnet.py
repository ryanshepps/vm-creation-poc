from ....Logger import Logger
from .ResourceGroup import ResourceGroup

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class Subnet:

    def __new__(
            cls, *, SubscriptionID: str, ResourceGroup: ResourceGroup,
            VirtualNetworkName: str, VMConfiguration: dict):
        logger = Logger(__name__)
        credentials = AzureCliCredential()
        network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        subnet_name = f"{VMConfiguration['name']}-subnet"
        subnet_parameters = {
            "address_prefix": "10.0.0.0/24",
        }

        logger.info(f"Provisioning Subnet for \
{VMConfiguration['name']}: \n\
resource_group_name: {ResourceGroup.name}\n\
virtual_network_name: {VirtualNetworkName}\n\
subnet_name: {subnet_name}\n\
subnet_parameters: \n\
{Logger.dict_to_formatted_string(subnet_parameters, 1)}")

        subnet_poller = network_client.subnets.begin_create_or_update(
            ResourceGroup.name,
            VirtualNetworkName,
            subnet_name,
            subnet_parameters
        )

        return subnet_poller.result()
