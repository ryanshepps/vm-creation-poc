from google.cloud import compute_v1


class Instance:

    def __create_labels(instance_configuration):
        formatted_labels = {}

        for key, label in instance_configuration.items():
            formatted_labels[key] = label.replace(" ", "-").lower()

        return {
            "team": formatted_labels["team"],
            "purpose": formatted_labels["purpose"],
            "os": formatted_labels["os"]
        }

    def __new__(cls, instance_configuration, disks, networks):
        instance = compute_v1.Instance()
        instance.disks = disks
        instance.network_interfaces = networks
        instance.name = instance_configuration["name"]
        instance.machine_type = \
            f'zones/{instance_configuration["zone"]}/machineTypes/f1-micro'
        instance.labels = cls.__create_labels(instance_configuration)
        instance.tags = {
            "items": ['linuxserver02-firewall']
        }

        if "description" in instance_configuration:
            instance.description = instance_configuration["description"]

        return instance
