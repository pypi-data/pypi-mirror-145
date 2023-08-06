class ValidationError(Exception):
    """
    Exception raised for errors in the type.

    Attributes:
        message -- explanation of the error
    """

    message = ""

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
