class PyAssemblyPaymentsException(Exception):
    pass


class PyAssemblyPaymentsNotImplementedException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsBadRequestException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsForbiddenException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsNotFoundException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsConflictException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsUnprocessableEntityException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsInternalErrorException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsInsufficientFundsException(PyAssemblyPaymentsException):
    pass


def handle422(response):
    """Parse 422 error message to return correct exception."""
    if (
        response.status_code == 422
        and "The account you're transacting from does not have enough funds available"
        in response.text
    ):
        return PyAssemblyPaymentsInsufficientFundsException
    return PyAssemblyPaymentsUnprocessableEntityException
