""" Test permission api"""
import unittest
import json
from app.test.base import BaseTestCase


class PemissionTests(BaseTestCase):
    """ Permission Test api class"""

    def test_get(self):
        """ smaple get call"""
        response = self.client.get(
            '/v1/permission',
            content_type='application/json'
        )
        self.assert200(response)

    def test_post_and_put(self):
        """ test post call"""
        response = self.client.post(
            '/v1/permission',
            data=json.dumps(dict(
                code='codeStr0159',
                name='codeStr0159',
                active=True
            )),
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))
        putId = json_response['data']['id']
        self.assert200(response)
        response = self.client.put(
            '/v1/permission/'+putId+'/',
            data=json.dumps(dict(
                active=True
            )),
            content_type='application/json'
        )
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
