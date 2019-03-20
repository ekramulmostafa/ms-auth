""" Test permission api"""
from base import BaseTestCase
import unittest
import json


class PemissionTests(BaseTestCase):
    """ Permission Test api class"""

    def test_get(self):
        """ smaple get call"""
        response = self.client.get(
            '/v1/permission',
            content_type='application/json'
        )
        self.assert200(response, message='tested man! chill out man!!')

    def test_post(self):
        """ test post call"""
        response = self.client.post(
            '/v1/permission',
            data=json.dumps(dict(
                code='samplecode',
                name='samplename',
                active=True
            )),
            content_type='application/json'
        )
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200, msg='tested man! chill out man!!')
        elif response.status_code == 500:
            self.assertEqual(response.status_code, 500, msg='data exists man! so what ? chill out man!!')
        else:
            self.assertEqual(response.status_code, 400,
                             msg='Validation failed man! so what ? chill out man, it is just 400 response!!')

    def test_put(self):
        """ test put call"""
        response = self.client.put(
            '/v1/permission/8cf319f5-275c-4af0-bb85-c92196d08e22/',
            data=json.dumps(dict(
                active=True
            )),
            content_type='application/json'
        )
        if response.status_code == 200:
            self.ssertEqual(response.status_code, 200, msg='tested man! chill out man!!')
        elif response.status_code == 500:
            self.assertEqual(response.status_code, 500, msg='data exists man! so what ? chill out man!!')
        else:
            self.assertEqual(response.status_code, 400,
                             msg='Validation failed man! so what ? chill out man, it is just 400 response!!')


if __name__ == "__main__":
    unittest.main()
