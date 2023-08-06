import json
from typing import Optional

from django.test import TestCase


class BaseApiTestCase(TestCase):

    def post(self, url: str, headers: dict, data: Optional[dict] = None):
        return self.client.post(
            url, **headers, data=json.dumps(data) if data else None,
            content_type='application/json'
        )

    def get(self, url: str, headers: dict):
        return self.client.get(
            url, **headers,
            content_type='application/json'
        )

    def put(self, url: str, headers: dict, data: Optional [dict] = None):
        return self.client.put(
            url, **headers, data=json.dumps(data) if data else None,
            content_type='application/json'
        )

    def patch(self, url: str, headers: dict, data: Optional[dict] = None):
        return self.client.patch(
            url, **headers, data=json.dumps(data) if data else None,
            content_type='application/json'
        )

    def delete(self, url: str, headers: dict):
        return self.client.delete(
            url, **headers,
            content_type='application/json'
        )

    def assertApiExceptionRaised(
            self: TestCase, response_data: dict, exception, strict=False
    ):
        error_code = exception.get_error_code()
        if not strict:
            error_code = int(error_code)
        expected_response = {
            'error_code': error_code
        }
        if 'extra' in response_data:
            expected_response['extra'] = exception.get_extra()
        if 'detail' in response_data:
            expected_response['detail'] = exception.detail
        elif 'details' in response_data:
            expected_response['details'] = exception.detail
        self.assertDictEqual(
            response_data,
            expected_response
        )

    def assertAllEqual(self, first, *args):
        self.assertTrue(
            all(
                first == i for i in args
            )
        )

    def assertAllNotEqual(self, first, *args):
        self.assertFalse(
            any(
                first == i for i in args
            )
        )
