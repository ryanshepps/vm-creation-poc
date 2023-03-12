from google.cloud import compute_v1


class Instance:

    def __create_labels(instance_configuration):
        formatted_labels = {}

        for key, label in instance_configuration.items():
            formatted_labels[key] = label.replace(" ", "-").lower()

        labels = {}

        if "team" in formatted_labels["team"]:
            labels["team"] = formatted_labels["team"]
        if "purpose" in formatted_labels["purpose"]:
            labels["purpose"] = formatted_labels["purpose"]
        if "os" in formatted_labels["os"]:
            labels["os"] = formatted_labels["os"]

        return labels

    def __new__(cls, instance_configuration, disks, networks):
        instance = compute_v1.Instance()
        instance.disks = disks
        instance.network_interfaces = networks
        instance.name = instance_configuration["name"]
        instance.machine_type = \
            f'zones/{instance_configuration["zone"]}/machineTypes/f1-micro'
        instance.labels = cls.__create_labels(instance_configuration)
        instance.tags = {
            "items": [f'{instance_configuration["name"]}-firewall']
        }

        if "description" in instance_configuration:
            instance.description = instance_configuration["description"]

        return instance
