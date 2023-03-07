import os
import json


# TODO: This class uses the CLI. Change it to use the SDK.
class Image:

    def __get_image_list() -> dict:
        stdout = os.popen("az vm image list")
        stdout_output = stdout.read()
        formatted_output = json.loads(stdout_output)
        return formatted_output

    def __get_image(images: list, urnAlias: str) -> dict:
        for image in images:
            if image["urnAlias"] == urnAlias:
                return image

        return None

    def __new__(cls, vm_configuration: dict):
        possible_vm_images = cls.__get_image_list()
        vm_image_spec = cls.__get_image(possible_vm_images, vm_configuration["image"])

        return {
            "publisher": vm_image_spec["publisher"],
            "offer": vm_image_spec["offer"],
            "sku": vm_image_spec["sku"],
            "version": vm_image_spec["version"]
        }
