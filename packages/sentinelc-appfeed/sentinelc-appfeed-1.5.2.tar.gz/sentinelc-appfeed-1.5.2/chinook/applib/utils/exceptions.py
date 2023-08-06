from .logger import eprint


class ValidationError(ValueError):
    def __init__(self, message):
        super().__init__(message)
        eprint(message)
