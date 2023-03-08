from .Network import Network
from .ResourceGroup import ResourceGroup
from classes.Logger import Logger

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient


class VirtualMachine:

    def __vm_conf_to_azure_conf(self, network: Network, vm_configuration: dict):
        return {
            "location": vm_configuration["location"],
            "storage_profile": {
                "image_reference": vm_configuration["image-reference"],
            },
            "hardware_profile": {
                "vm_size": "Standard_DS1_v2"
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": network.id
                    },
                ],
            },
            "os_profile": {
                "computer_name": vm_configuration["name"],
                "admin_username": vm_configuration["admin-username"],
                "admin_password": vm_configuration["admin-password"],
            }
        }

    def __init__(
            self, *, SubscriptionID: str, ResourceGroup: ResourceGroup,
            Network: Network, VM_Configuration: dict):
        logger = Logger(__name__)

        azure_vm_configuration = self.__vm_conf_to_azure_conf(Network, VM_Configuration)
        logger.info(f"Creating VM {VM_Configuration['name']}: \n\
{Logger.dict_to_formatted_string(azure_vm_configuration)}")

        credentials = AzureCliCredential()
        compute_client = ComputeManagementClient(credentials, SubscriptionID)
        vm_creation_poller = compute_client.virtual_machines \
            .begin_create_or_update(
                resource_group_name=ResourceGroup.name,
                vm_name=VM_Configuration["name"],
                parameters=azure_vm_configuration)
        self.result = vm_creation_poller.result()

        logger.info(f"VM {VM_Configuration['name']} successfully created.")
