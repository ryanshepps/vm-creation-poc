from google.cloud import compute_v1


class Network:

    def __new__(cls):
        network_interface = compute_v1.NetworkInterface()
        network_interface.name = "global/networks/default"

        external_access = compute_v1.AccessConfig()
        external_access.network_tier = \
            external_access.NetworkTier.STANDARD.name

        network_interface.access_configs = [external_access]

        return network_interface
