import logging


class Logger:

    @staticmethod
    def dict_to_formatted_string(dict_to_format: dict, level: int = 0):
        formatted_string = ""

        cur_level_spaces = " " * level * 2
        for key, value in dict_to_format.items():
            if type(value) is str:
                # Quote string with ""
                if key == "admin_password":
                    # Hide admin password
                    formatted_string += f"{cur_level_spaces}{key}: <hidden>\n"
                else:
                    formatted_string += f"{cur_level_spaces}{key}: \"{value}\"\n"
            elif type(value) is dict:
                # Format non-empty dict by calling function recursively
                if len(value.items()) == 0:
                    # Empty dict, print {}
                    formatted_string += f"{cur_level_spaces}{key}: {{}}\n"
                else:
                    formatted_string += \
                        f"{cur_level_spaces}{key}: {{\n\
{Logger.dict_to_formatted_string(value, level + 1)}\n\
{cur_level_spaces}}}\n"
            else:
                # Unformatted value
                formatted_string += f"{cur_level_spaces}{key}: {value}\n"

        # Remove EOL newline
        formatted_string = formatted_string[:-1]

        return formatted_string

    def __new__(cls, Name):
        stdout_formatter = logging.Formatter(
            '[%(asctime)s] %(name)-40s%(levelname)-6s%(message)s')
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(stdout_formatter)

        logger = logging.getLogger(Name)
        logger.addHandler(stdout_handler)
        logger.setLevel(logging.INFO)

        return logger
