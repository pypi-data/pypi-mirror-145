MODULE_NOT_FOUND_MSG = "Module not found"


class ApiCallError(Exception):
    """
    Raised when API call fails
    """
    def __init__(self, message, details):
        self.message = message
        self.details = details
        super().__init__(self.message)
