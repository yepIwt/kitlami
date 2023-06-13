from typing import Mapping


class ApiException(Exception):
    """
    Base class for API exceptions
    """

    status_code: int = 500
    message: str = "Упс! Что-то пошло не так ;("

    def __init__(
        self,
        message: str | None = None,
        payload: Mapping | None = None,
        exception_class: str | None = None,
    ):
        self.message = message or self.message
        self.payload = payload
        self.exception_class = exception_class

    def _type(self):
        return self.__class__.__name__

    def to_json(self) -> Mapping:
        return {"code": self.status_code, "message": self.message, "payload": self.payload}


class ServerError(ApiException):
    status_code = 500
    message = "Упс! Что-то пошло не так ;("


class NotFoundError(ApiException):
    status_code = 404
    message = "Not Found"


class ObjectNotFoundError(ApiException):
    status_code = 404
    message = "Object Not Found"


class BadRequestError(ApiException):
    status_code = 400


class ValidationError(ApiException):
    status_code = 400
