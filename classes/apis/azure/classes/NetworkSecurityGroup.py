from ....Logger import Logger
from .ResourceGroup import ResourceGroup
from .SecurityRule import SecurityRule

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class NetworkSecurityGroup:

    def __new__(
            cls, *, SubscriptionID: str, ResourceGroup: ResourceGroup,
            VMConfiguration: dict):
        logger = Logger(__name__)

        credentials = AzureCliCredential()
        network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        network_security_group_name = f"{VMConfiguration['name']}-nsg"
        network_security_group_parameters = {
            "location": VMConfiguration["location"],
        }

        logger.info(f"Provisioning Network Security Group for \
{VMConfiguration['name']}: \n\
resource_group_name: {ResourceGroup.name}\n\
network_security_group_name: {network_security_group_name}\n\
virtual_network_parameters: \n\
{Logger.dict_to_formatted_string(network_security_group_parameters, 1)}")

        nsg_poller = network_client.network_security_groups\
            .begin_create_or_update(
                ResourceGroup.name,
                network_security_group_name,
                network_security_group_parameters
            )

        nsg_poller.result()

        security_rule = SecurityRule(
            SubscriptionID=SubscriptionID, ResourceGroup=ResourceGroup,
            NetworkSecurityGroupName=network_security_group_name,
            VMConfiguration=VMConfiguration)
        network_security_group_parameters["security_rules"] = [security_rule]

        logger.info(f"Adding Security Rule {security_rule.name} to \
{network_security_group_name}")

        nsg_poller = network_client.network_security_groups\
            .begin_create_or_update(
                ResourceGroup.name,
                network_security_group_name,
                network_security_group_parameters
            )

        return nsg_poller.result()
