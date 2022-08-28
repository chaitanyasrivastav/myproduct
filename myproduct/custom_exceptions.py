class BaseException(Exception):
    def __init__(self, message):
        self.message = message

class MethodNotAllowedError(BaseException):
    status_code = 405
    error_code = "METHOD_NOT_ALLOWED"

class AlreadyExistsError(BaseException):
    status_code = 409
    error_code = "ALREADY_EXISTS"

class NotFoundError(BaseException):
    status_code = 404
    error_code = "NOT_FOUND"

class InternalServerError(BaseException):
    pass

