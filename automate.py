from classes.apis.azure.AzureComposer import AzureComposer
from classes.apis.azure.AzureValidator import AzureValidator
from classes.apis.gcloud.GCloudComposer import GCloudComposer
from classes.apis.gcloud.GCloudValidator import GCloudValidator
from classes.apis.generic.Parser import Parser

parser = Parser()

validator = GCloudValidator()
composer = GCloudComposer(Parser=parser, Validator=validator)
composer.compose_from_file("./example/input/gcp.conf")

validator = AzureValidator()
composer = AzureComposer(Parser=parser, Validator=validator)
composer.compose_from_file("./example/input/azure.conf")
