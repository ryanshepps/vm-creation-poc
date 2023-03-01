from google.cloud import compute_v1


class BootDisk:

    def __new__(cls, instance_configuration):
        images_client = compute_v1.ImagesClient()
        boot_image = images_client.get(
            image=instance_configuration["image"],
            project=instance_configuration["imageproject"])

        boot_disk_params = compute_v1.AttachedDiskInitializeParams()
        boot_disk_params.source_image = boot_image.self_link
        boot_disk_params.disk_size_gb = boot_image.disk_size_gb

        disk_type = \
            f'zones/{instance_configuration["zone"]}/diskTypes/pd-standard'
        boot_disk_params.disk_type = disk_type

        boot_disk = compute_v1.AttachedDisk()
        boot_disk.initialize_params = boot_disk_params
        boot_disk.auto_delete = True
        boot_disk.boot = True

        return boot_disk
