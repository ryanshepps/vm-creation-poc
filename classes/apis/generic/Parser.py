import configparser

from classes.abstractions.Parser import Parser
from classes.Logger import Logger


class Parser(Parser):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)

    def parse(self, file_location: str) -> dict:
        self.logger.debug(f'parse(file_location={file_location})')
        parsed_file = list()

        config = configparser.ConfigParser()
        config.read(file_location)

        for section in config.sections():
            parsed_section = dict()
            for item in config.items(section):
                parsed_section[item[0]] = item[1]
            parsed_file.append(parsed_section)

        self.logger.debug(f'returning: {parsed_file}')
        return parsed_file
