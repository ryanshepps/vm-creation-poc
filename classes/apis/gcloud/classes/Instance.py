from google.cloud import compute_v1


class Instance:

    def __new__(cls, instance_configuration, disks, networks):
        instance = compute_v1.Instance()
        instance.disks = disks
        instance.network_interfaces = networks
        instance.name = instance_configuration["name"]
        instance.machine_type = \
            f'zones/{instance_configuration["zone"]}/machineTypes/f1-micro'

        return instance
