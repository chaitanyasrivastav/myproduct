class BaseException(Exception):
    def __init__(self, message):
        self.message = message



class MethodNotAllowedError(BaseException):
    status_code = 405
    error_code = "METHOD_NOT_ALLOWED"

class AlreadyExistsError(BaseException):
    status_code = 409
    error_code = "ALREADY_EXISTS"

class BadRequestError(BaseException):
    status_code = 400
    error_code = "BAD_REQUEST"

class InternalServerError(BaseException):
    pass

