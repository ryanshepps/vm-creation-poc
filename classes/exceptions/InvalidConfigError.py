class InvalidConfigError(Exception):

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        else:
            self.message = 'Configuration is invalid.'

        super().__init__(self.message)
