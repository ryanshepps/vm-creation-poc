from ....Logger import Logger
from .ResourceGroup import ResourceGroup

from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient


class SecurityRule:

    def __new__(
            cls, *, SubscriptionID: str, ResourceGroup: ResourceGroup,
            NetworkSecurityGroupName: str,
            VMConfiguration: dict):
        logger = Logger(__name__)

        credentials = AzureCliCredential()
        network_client = NetworkManagementClient(
            credentials, SubscriptionID)

        security_rule_name = f"{VMConfiguration['name']}-security-rule"
        security_rule_parameters = {
            "source_port_range": "*",
            "source_address_prefix": "*",
            "destination_address_prefix": "*",
            "destination_port_ranges": VMConfiguration["ports"].split(", "),
            "protocol": "Tcp",
            "access": "Allow",
            "direction": "Inbound",
            "priority": 100,
            "name": security_rule_name
        }

        logger.info(f"Provisioning Security Rule for \
{VMConfiguration['name']}: \n\
resource_group_name: {ResourceGroup.name}\n\
security_rule_name: {security_rule_name}\n\
security_rule_parameters: \n\
{Logger.dict_to_formatted_string(security_rule_parameters, 1)}")

        nsg_poller = network_client.security_rules\
            .begin_create_or_update(
                ResourceGroup.name,
                NetworkSecurityGroupName,
                security_rule_name,
                security_rule_parameters
            )

        return nsg_poller.result()
