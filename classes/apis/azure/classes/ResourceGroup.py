from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient


class ResourceGroup:

    def __new__(cls, subscription_id: str, vm_configuration: object):
        credential = AzureCliCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)

        resource_group_name = vm_configuration["resource-group"]
        resource_group_location = vm_configuration["location"]

        resource_group_result = \
            resource_client.resource_groups.create_or_update(
                resource_group_name, {"location": resource_group_location}
            )

        return resource_group_result
