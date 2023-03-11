from ....Logger import Logger
from .Network import Network

from google.cloud import compute_v1


class Firewall:

    def __new__(cls, network: Network, instance_configuration: dict):
        logger = Logger(__name__)

        firewall_rule_name = f"{instance_configuration['name']}-firewall"

        allowed_ports = compute_v1.Allowed()
        allowed_ports.I_p_protocol = "tcp"
        allowed_ports.ports = instance_configuration["ports"].split(", ")

        firewall_rule = compute_v1.Firewall()
        firewall_rule.name = firewall_rule_name
        firewall_rule.direction = "INGRESS"
        firewall_rule.allowed = [allowed_ports]
        firewall_rule.source_ranges = ["0.0.0.0/0"]
        firewall_rule.target_tags = [firewall_rule_name]
        firewall_rule.network = network.name
        firewall_rule.description = f"Allows TCP traffic on port(s) \
{instance_configuration['ports']} from Internet."

        logger.info(f"Creating firewall: \n{str(firewall_rule)}")
        firewall_client = compute_v1.FirewallsClient()
        operation = firewall_client.insert(
            project=instance_configuration["project"],
            firewall_resource=firewall_rule
        )
        operation.result()  # Wait for operation to complete synchronously
