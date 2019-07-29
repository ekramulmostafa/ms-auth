"""Test Role"""

import unittest
import json
from flask import url_for
from app.test import BaseTest


class PermissionTests(BaseTest):
    """ Permission Test api class """

    def test_insert_update(self):
        """ insert roles then update and then get the updated role and insert multiple roles """

        url = url_for('auth.permission_permission_list')

        params = {
            'data': {
                'name': 'test permission',
                'active': True,
                "code": "TEST_CONTENT_CREATE"
            }
        }
        role_data = json.dumps(params)

        response = self.client.post(
            url,
            data=role_data,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))['data']
        # print('peeeeeeeeeeeeeep')
        # print(json_response)
        post_id = json_response['id']


        self.assertEqual(response.status_code, 201)

        params = {
            'data': {
                "name": "test permission update",
                "active": False,
                "code": "TEST_CONTENT_CREATE_UPDATE",
                "updated_by": "Test_1238123"
            }
        }

        role_data = json.dumps(params)

        url = url_for('auth.permission_permission_detail', uuid=post_id)

        response = self.client.put(
            url,
            data=role_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))['data']

        self.assertEqual(json_response['code'], 'TEST_CONTENT_CREATE_UPDATE')

        # check readonly fields value changing
        self.assertIsNotNone(json_response['updated_at'])
        self.assertNotEqual(json_response['created_at'], json_response['updated_at'])

    def test_get_all_permission(self):
        """ Get all permission and also filtered permission """
        url = url_for('auth.permission_permission_list')
        params = [
            {
                'name': 'test_permission1',
                'active': True,
                "code": "TEST_PERMISSION1",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_permission2',
                'active': False,
                "code": "TEST_PERMISSION2",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_permission3',
                'active': True,
                "code": "TEST_PERMISSION3",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps({"data": param})

            response = self.client.post(
                url,
                data=role_data,
                content_type='application/json'
            )

        response = self.client.get(
            url,
            content_type='application/json'
        )
        self.assert200(response)

    def test_filter_data(self):
        """ Test filter data with filtered string """
        url = url_for('auth.permission_permission_list')
        params = [
            {
                'name': 'test_permission1',
                'active': True,
                "code": "TEST_PERMISSION1",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_permission2',
                'active': False,
                "code": "TEST_PERMISSION2",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_permission3',
                'active': True,
                "code": "TEST_PERMISSION3",
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps({"data": param})

            response = self.client.post(
                url,
                data=role_data,
                content_type='application/json'
            )

        extra_url = url + '?active=1'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))['data']
        self.assertEqual(len(json_response), 2)

        extra_url = url + '?created_at=2019-07-28,2019-07-30'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))['data']
        self.assertEqual(len(json_response), 3)

if __name__ == "__main__":
    unittest.main()
