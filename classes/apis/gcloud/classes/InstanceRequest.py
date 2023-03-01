from google.cloud import compute_v1


class InstanceRequest:

    def __new__(cls, instance_configuration, instance):
        instance_request = compute_v1.InsertInstanceRequest()
        instance_request.instance_resource = instance
        instance_request.zone = instance_configuration["zone"]
        instance_request.project = instance_configuration["project"]

        return instance_request
