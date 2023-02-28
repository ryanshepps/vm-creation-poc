import logging


class Logger:

    def __new__(cls, Name):
        stdout_formatter = logging.Formatter(
            '[%(asctime)s] %(name)-40s%(levelname)-6s%(message)s')
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(stdout_formatter)

        logger = logging.getLogger(Name)
        logger.addHandler(stdout_handler)
        logger.setLevel(logging.DEBUG)

        return logger
