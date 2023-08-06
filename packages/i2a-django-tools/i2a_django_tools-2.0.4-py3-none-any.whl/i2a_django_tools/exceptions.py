from typing import Type

from django.utils.translation import gettext_lazy
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomApiException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = gettext_lazy("Request cannot be processed.")
    error_code = None
    wrapped_exception = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = (self.detail, )

    def get_extra(self):
        pass

    def get_error_code(self):
        return self.error_code

    @classmethod
    def wrap(cls, exception: Type['CustomApiException']):
        wrapper = cls(*exception.args)
        wrapper.wrapped_exception = exception
        return wrapper
