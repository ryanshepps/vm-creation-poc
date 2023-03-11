from .VirtualNetwork import VirtualNetwork
from .ResourceGroup import ResourceGroup
from .Subnet import Subnet
from ....Logger import Logger

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class Network:

    def __new__(
            cls, *, SubscriptionID: int, ResourceGroup: ResourceGroup,
            VMConfiguration: dict):
        logger = Logger(__name__)

        credentials = AzureCliCredential()
        network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        virtual_network = VirtualNetwork(
            SubscriptionID=SubscriptionID, ResourceGroup=ResourceGroup,
            VMConfiguration=VMConfiguration)
        subnet = Subnet(
            SubscriptionID=SubscriptionID, ResourceGroup=ResourceGroup,
            VirtualNetworkName=virtual_network.name,
            VMConfiguration=VMConfiguration)

        ip_configuration_name = f"{VMConfiguration['name']}-ip-config"
        network_interface_name = f"{VMConfiguration['name']}-network-interface"
        network_interface_parameters = {
            "location": VMConfiguration["location"],
            "ip_configurations": [
                {
                    "name": ip_configuration_name,
                    "subnet": {
                        "id": subnet.id,
                    },
                }
            ]
        }

        logger.info(f"Provisioning Network Interface for \
{VMConfiguration['name']}: \n\
resource_group_name: {ResourceGroup.name}\n\
network_interface_name: {network_interface_name}\n\
network_interface_parameters: \n\
{Logger.dict_to_formatted_string(network_interface_parameters, 1)}")

        network_interface_poller = network_client.network_interfaces.begin_create_or_update(
            ResourceGroup.name,
            network_interface_name,
            network_interface_parameters
        )

        return network_interface_poller.result()
