""" Test permission api"""
import unittest
import json
from app.test.base import BaseTestCase


class PemissionTests(BaseTestCase):
    """ Permission Test api class"""

    def test_get(self):
        """ Permission get call
        Permission search call
        Permission filter call
        Permission limit & offset
        """
        response = self.client.get(
            '/v1/permission',
            content_type='application/json'
        )
        self.assert200(response)
        response = self.client.get(
            '/v1/permission?search=cssfdf',
            content_type='application/json'
        )
        self.assert200(response)
        response = self.client.get(
            '/v1/permission?active=true',
            content_type='application/json'
        )
        self.assert200(response)
        response = self.client.get(
            '/v1/permission?limit=1&offset=1',
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
        put_id = json_response['data']['id']
        self.assert200(response)
        response = self.client.put(
            '/v1/permission/'+put_id+'/',
            data=json.dumps(dict(
                active=True
            )),
            content_type='application/json'
        )
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
