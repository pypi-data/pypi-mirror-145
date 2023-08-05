import logging
import traceback
from typing import List, Mapping

_Logger = logging.getLogger(__name__)

# ---- HTTP-related
class ClientError(Exception):
    """Client request is incorrect."""

    pass


class AuthenticationError(Exception):
    """Failed to authenticate user."""

    pass


class ForbiddenError(Exception):
    """Forbidden access to resource."""

    pass


class NotFoundError(Exception):
    """Resource not found."""

    pass


class MethodNotAllowed(Exception):
    """Method not allowed for resource."""

    pass


class ExpiredSessionError(Exception):
    """Current user session has expired. Login required."""

    pass


class ExpiredTokenError(Exception):
    """Access token has expired, refresh required."""

    pass


class InternalServerError(Exception):
    """Server reported internal error."""

    pass


class BadGatewayError(Exception):
    """Upstream server reported internal error."""

    pass


class ServiceUnavailableError(Exception):
    """Service is not available."""

    pass


class GatewayTimeoutError(Exception):
    """Upstream server did not respond in time."""

    pass


class UnknownError(Exception):
    """Unknown error."""

    pass


class UnreachableError(Exception):
    """Code is unreachable."""

    pass


class LogicError(Exception):
    """Logical inconsistency."""

    pass


class CriticalError(Exception):
    """Critical error."""

    pass


class GCPError(Exception):
    """GCP reported error."""

    pass


class HTTPRequestError(Exception):
    """General error in the HTTP request."""

    pass


class RuntimeError(RuntimeError):
    """Error depending on run-time conditions."""

    pass


class ValueError(ValueError):
    """Incorrect value."""

    pass


class NotImplementedError(NotImplementedError):
    """Feature not implemented."""

    pass


class UnhandledError(Exception):
    """Error not contemplated."""

    pass


class TimeoutError(TimeoutError):
    """Time taken was more than expected."""

    pass


class AcquireResourceError(Exception):
    """Failure in resource acquisition."""

    pass


class VersionError(Exception):
    """Incompatibility between client and server API versions"""

    pass


class MultipleError(Exception):
    """Container for multiple errors."""

    def __init__(self, *errors):
        self.errors: List[Exception] = [e for e in errors]


_HTTPCodeToException: Mapping[int, type] = {
    400: ClientError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowed,
    410: VersionError,
    440: ExpiredSessionError,
    498: ExpiredTokenError,
    500: InternalServerError,
    501: NotImplementedError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
}


_ExceptionToHTTPCode: Mapping[str, int] = {
    t.__name__: c for c, t in _HTTPCodeToException.items()
}


def http_code_to_exception(code: int, text: str, default: type) -> Exception:
    """Returns an exception object from integer code and text content

    Args:
        code (int): HTTP code
        text (str): Error text
        default (type): Default error type in case ``code`` do not match any error.

    Returns:
        Exception: Error associated to ``code``
    """

    if code in _HTTPCodeToException:
        return _HTTPCodeToException[code](text)
    else:
        return default(text)


def exception_type_to_http_code(exc_type: str) -> int:
    """Returns an error code for any exception type

    Args:
        exc_type (str): A type of exception

    Returns:
        int: Error code associated to type, or 500 if type is not associated to a HTTP error.
    """

    return _ExceptionToHTTPCode[exc_type] if exc_type in _ExceptionToHTTPCode else 500


def exception_to_http_code(exc: Exception) -> int:
    """Returns a HTTP error code from an exception object.

    Args:
        exc (Exception): Exception object

    Returns:
        int: Error code
    """

    return exception_type_to_http_code(type(exc).__name__)


def _single_handler(exc: Exception, is_debug: bool) -> Mapping[str, str]:
    """Creates a dict representation of an exception object, possibly appending traceback info.

    Args:
        exc (Exception): Exception object
        is_debug (bool): Whether to append traceback info.

    Returns:
        Mapping[str, str]: Dict representation of exception.
    """

    assert not isinstance(exc, MultipleError)

    return {
        "type": type(exc).__name__,
        "content": str(exc) if not "html" in str(exc) else "Omitted HTML content",
        "code": exception_to_http_code(exc),
        "traceback": f'{"".join(traceback.format_tb(exc.__traceback__))}'
        if is_debug and isinstance(exc, Exception)
        else "hidden",
    }


def error_handler(*excs) -> Mapping[str, Mapping[str, str]]:
    """Creates a dict representation of multiple exception objects.

    Returns:
        Mapping[str,Mapping[str,str]]: Dict representation of exceptions

    Notes:
        Error handler returning a json with formatted errors. Input errors may be reordered if some of them are ``MultipleError``.
    """

    is_debug = logging.root.level <= logging.DEBUG

    ret = {"errors": []}

    # Create descriptions for each of the single errors
    ret["errors"] += [
        _single_handler(exc, is_debug)
        for exc in excs
        if not isinstance(exc, MultipleError)
    ]

    # Log single errors
    for single_err in ret["errors"]:
        if single_err["type"] == CriticalError.__name__:
            _Logger.critical(single_err)
        elif exception_type_to_http_code(single_err["type"]) >= 500:
            _Logger.error(single_err)
        else:
            _Logger.warning(single_err)

        if is_debug:
            for k in ["type", "content", "traceback"]:
                _Logger.debug(single_err[k])

    # Unfold single errors within multiple errors
    ret["errors"] += [
        exc_desc
        for multiple in excs
        if isinstance(multiple, MultipleError)
        for exc_desc in error_handler(*multiple.errors)["errors"]
    ]

    return ret


def make_errors_from_json(*errs_json) -> Exception:
    """Creates an exception object from multiple dict representation of errors.

    Returns:
        Exception: Exception object encapsulating inputs.
    """

    err_objs = []
    for err_json in errs_json:

        assert all([rk in err_json for rk in ["type", "content"]])

        err_msg = err_json["content"]
        if "traceback" in err_json:
            err_msg += "\nOriginal traceback: " + err_json["traceback"]

        if err_json["type"] in globals():
            # Interpret error as one of our defined classes in this file
            err_objs.append(globals()[err_json["type"]](err_msg))
        else:
            err_objs.append(
                UnhandledError(
                    "Original type: "
                    + err_json["type"]
                    + "\nOriginal content: "
                    + err_msg
                )
            )

    if len(err_objs) == 1:
        return err_objs[0]
    else:
        return MultipleError(*err_objs)


def raise_from_list(exceptions: List[Exception]):
    """Collapse all exceptions in list into a single exception.

    Args:
        exceptions (List[Exception]): List of exceptions.

    Raises:
        Exception: Single exception in list
        MultipleError: Capturing all exceptions in list
    """

    if len(exceptions) == 1:
        raise exceptions[0]
    elif len(exceptions) > 1:
        raise MultipleError(*exceptions)
