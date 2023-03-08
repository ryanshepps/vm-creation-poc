import datetime
import os
import shutil

from .Logger import Logger


class VMDocumenter:

    def __init__(self) -> None:
        self.logger = Logger(__name__)

    def __document_vm(
            self, vm_documentation: str, vm_doc_file_location, time_now: str):
        os.makedirs(os.path.dirname(vm_doc_file_location), exist_ok=True)

        vm_doc = open(vm_doc_file_location, "w")
        vm_doc.write(f"date: {time_now}")
        vm_doc.write(f"script_runner: {os.getlogin()}\n")
        vm_doc.write(f"{vm_documentation}\n")

        self.logger.info(f"Documented VM to file {vm_doc_file_location}")

        vm_doc.close()

    def __document_vm_config(
            self, vm_config_location: str, vm_config_doc_location: str,
            time_now: str):
        os.makedirs(
            os.path.dirname(vm_config_doc_location), exist_ok=True)

        shutil.copy(vm_config_location, vm_config_doc_location)

        self.logger.info(
            f"Documented VM configuration to file \
{vm_config_doc_location}")

    def document(
            self, vm_documentation: str, vm_doc_file_location: str,
            vm_config_location: str, vm_config_doc_file_location: str):
        now = datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S')

        self.__document_vm(vm_documentation, vm_doc_file_location, now)
        self.__document_vm_config(
            vm_config_location, vm_config_doc_file_location, now)
