class MethodNotAllowedError(Exception):
    status_code = 405
    error_code = "METHOD_NOT_ALLOWED"

    def __init__(self, message):
        self.message = message

class AlreadyExistsError(Exception):
    status_code = 409
    error_code = "ALREADY_EXISTS"

    def __init__(self, message):
        self.message = message

class InternalServerError(Exception):
    pass

