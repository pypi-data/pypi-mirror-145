import datetime
from json import JSONDecodeError
from urllib.parse import urlencode, quote_plus

import requests

from assembly_payments.exceptions import (
    PyAssemblyPaymentsException,
    PyAssemblyPaymentsNotImplementedException,
    PyAssemblyPaymentsBadRequestException,
    PyAssemblyPaymentsForbiddenException,
    PyAssemblyPaymentsNotFoundException,
    PyAssemblyPaymentsConflictException,
    PyAssemblyPaymentsInternalErrorException,
    handle422,
)


class BaseService:
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"

    def __init__(
        self, get_auth=None, base_url=None, auth_url=None, beta_url=None, logging=False
    ):
        self.get_auth = get_auth
        self.endpoint = None
        self.base_url = base_url
        self.auth_url = auth_url
        self.beta_url = beta_url
        self.logging = logging

    def _execute(self, method, endpoint, data=None, headers=None, url=None):
        if headers is None:
            headers = dict(Authorization=f"Bearer {self.get_auth()}")

        if url is None:
            url = self.base_url

        response = getattr(requests, method)(
            f"{url}{endpoint}", json=data, headers=headers
        )

        if self.logging:
            print(method.upper(), endpoint, response.status_code, response.text)

        self._handle_exceptions(response)
        if response.content:
            return response.json()
        return

    def _handle_exceptions(self, response):
        exc_classes = {
            400: PyAssemblyPaymentsBadRequestException,
            403: PyAssemblyPaymentsForbiddenException,
            404: PyAssemblyPaymentsNotFoundException,
            409: PyAssemblyPaymentsConflictException,
            422: handle422,  # parse error message before returning correct error message.
            500: PyAssemblyPaymentsInternalErrorException,
            501: PyAssemblyPaymentsInternalErrorException,
            502: PyAssemblyPaymentsInternalErrorException,
            503: PyAssemblyPaymentsInternalErrorException,
            504: PyAssemblyPaymentsInternalErrorException,
        }

        exc_class = exc_classes.get(response.status_code)
        if exc_class:
            try:
                data = response.json()
                if not isinstance(exc_class, PyAssemblyPaymentsException):
                    # if not an Exception, it's an callable and needs to be called.
                    exc_class = exc_class(response)
            except JSONDecodeError:
                data = response.text
            raise exc_class(data)

    def append_query_params(self, endpoint: str, query_params: dict) -> str:
        datetimes = dict()

        for key, value in query_params.copy().items():
            if isinstance(value, datetime.datetime):
                datetimes[quote_plus(key)] = query_params.pop(key).isoformat()

        datetime_params = ""
        if datetimes:
            datetime_params = "&" + "&".join(
                f"{key}={value}" for key, value in datetimes.items()
            )

        return f"{endpoint}?{urlencode(query_params)}{datetime_params}"

    def list(self, *args, **kwargs):
        raise PyAssemblyPaymentsNotImplementedException(
            f"{self.__class__} does not implement list. Please raise an issue or PR if you'd like it implemented."
        )

    def get(self, *args, **kwargs):
        raise PyAssemblyPaymentsNotImplementedException(
            f"{self.__class__} does not implement get. Please raise an issue or PR if you'd like it implemented."
        )

    def create(self, **kwargs):
        raise PyAssemblyPaymentsNotImplementedException(
            f"{self.__class__} does not implement create. Please raise an issue or PR if you'd like it implemented."
        )

    def update(self, **kwargs):
        raise PyAssemblyPaymentsNotImplementedException(
            f"{self.__class__} does not implement update. Please raise an issue or PR if you'd like it implemented."
        )

    def delete(self, *args, **kwargs):
        raise PyAssemblyPaymentsNotImplementedException(
            f"{self.__class__} does not implement delete. Please raise an issue or PR if you'd like it implemented."
        )
