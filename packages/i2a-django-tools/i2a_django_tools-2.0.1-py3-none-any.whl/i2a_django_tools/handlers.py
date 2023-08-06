from typing import Type, Dict, Any

from django.http.response import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from exceptions import CustomApiException


def api_exception_handler(exc: Type[Exception], context: Dict[str, Any]):
    """
    Mostly copied from rest-framework

    Returns the response that should be used for any given exception.

    Can append 'extra' field on returned data.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        # check what is inside detail.
        if isinstance(exc.detail, dict):
            data = exc.detail
        if isinstance(exc.detail, list):
            data = {'details': exc.detail}
        else:  # exc detail is string.
            data = {'detail': exc.detail}

        if isinstance(exc, CustomApiException):
            extra = exc.get_extra()
            if extra:
                data['extra'] = extra
            error_code = exc.get_error_code()
            if error_code:
                parse_error_code_to_int = True
                if parse_error_code_to_int:
                    data['error_code'] = int(error_code)
                else:
                    data['error_code'] = error_code
        if isinstance(exc, ValidationError):
            assert 'error_code' not in data
            data['error_code'] = 400001
        views.set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None
