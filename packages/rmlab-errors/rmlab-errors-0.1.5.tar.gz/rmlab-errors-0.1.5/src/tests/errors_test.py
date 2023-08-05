import pytest
import importlib
import inspect
import json

from rmlab_errors import (
    AuthenticationError,
    ClientError,
    InternalServerError,
    LogicError,
    MultipleError,
    UnhandledError,
    _single_handler,
    error_handler,
    exception_to_http_code,
    exception_type_to_http_code,
    http_code_to_exception,
    _ExceptionToHTTPCode,
    make_errors_from_json,
)


def test_error_json_conversions():
    """Test correct json parsing of every custom exception class in errors module"""

    members = [
        tuple((name, obj))
        for name, obj in inspect.getmembers(importlib.import_module("rmlab_errors"))
        if "Error" in name and "MultipleError" != name
    ]

    class NeverSeenError(Exception):
        pass

    members.append(tuple((NeverSeenError.__name__, NeverSeenError)))

    json_errors = []
    for name, obj in members:
        cnt = "Error msg"
        err = obj(cnt)
        err_json = _single_handler(err, is_debug=False)

        assert "type" in err_json
        assert "content" in err_json
        assert "code" in err_json
        assert "traceback" in err_json

        assert err_json["content"] == cnt
        assert err_json["code"] == exception_to_http_code(err)

        json_errors.append(err_json)

    multiple_exc = make_errors_from_json(*json_errors)
    assert type(multiple_exc).__name__ == "MultipleError"

    for exc, (name, obj) in zip(multiple_exc.errors, members):
        if name != "NeverSeenError":
            assert type(exc).__name__ == name
        else:
            # Not custom error => falls back to UnhandledError
            assert type(exc).__name__ == "UnhandledError"


def test_type_recover():
    """Test recovery of error type from string"""

    str_exc = LogicError.__name__

    type_exc = getattr(importlib.import_module("rmlab_errors"), str_exc)

    assert type_exc == LogicError


def test_multiple():
    """Test conversions involving MultipleError"""

    client_exc = ClientError("my client error")
    auth_exc = AuthenticationError("my auth error")
    rt_exc = RuntimeError("my rt error")

    multiple_exc = MultipleError(client_exc, auth_exc, rt_exc)

    assert len(multiple_exc.errors) == 3

    with pytest.raises(AssertionError):
        _single_handler(multiple_exc, is_debug=False)

    multiple_json = error_handler(multiple_exc)

    individual_json = error_handler(client_exc, auth_exc, rt_exc)

    assert json.dumps(multiple_json) == json.dumps(individual_json)


def test_http_code_to_exception():
    """Test conversions based on http codes"""

    all_exc_types = [
        name
        for name, obj in inspect.getmembers(importlib.import_module("rmlab_errors"))
        if "Error" in name and "MultipleError" != name
    ]

    all_exc_types.append("NeverSeenException")

    for exc_type in all_exc_types:

        code = exception_type_to_http_code(exc_type)

        ret_exc = http_code_to_exception(code, "content", UnhandledError)

        if exc_type in _ExceptionToHTTPCode:
            assert exc_type == type(ret_exc).__name__
            assert str(ret_exc) == "content"
        else:
            type(ret_exc).__name__ == InternalServerError.__name__
            assert str(ret_exc) == "content"
