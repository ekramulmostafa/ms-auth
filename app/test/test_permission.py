"""Test Role"""

import unittest
import json
from datetime import datetime, timedelta
from flask import url_for
from app.test import BaseTest


class PermissionTests(BaseTest):
    """ Permission Test api class """

    def test_insert_update(self):
        """ insert roles then update and then get the updated role and insert multiple roles """

        permission_url = url_for('auth.permission_permission_list')

        params = {
            'data': {
                'name': 'test permission',
                'active': True,
                "code": "TEST_CONTENT_CREATE"
            }
        }

        role_data = json.dumps(params)

        response = self.client.post(
            permission_url,
            data=role_data,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))['data']
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

        permission_data = json.dumps(params)

        url = url_for('auth.permission_permission_detail', uuid=post_id)

        permission_response = self.client.put(
            url,
            data=permission_data,
            content_type='application/json'
        )
        self.assertEqual(permission_response.status_code, 200)
        permission_response = self.client.get(
            url,
            content_type='application/json'
        )

        json_response = json.loads(permission_response.get_data(as_text=True))['data']

        self.assertEqual(json_response['code'], 'TEST_CONTENT_CREATE_UPDATE')

        # check readonly fields value changing
        self.assertIsNotNone(json_response['updated_at'])
        self.assertNotEqual(json_response['created_at'], json_response['updated_at'])

    def test_get_all_permission(self):
        """ Get all permission and also filtered permission """
        permission_url = url_for('auth.permission_permission_list')
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
                'created_by': 'Test_123812378174',
                'updated_by': 'Test_123812378174'
            }
        ]

        for prm in params:
            role_data = json.dumps({'data': prm})

            self.client.post(
                permission_url,
                data=role_data,
                content_type='application/json'
            )

        response = self.client.get(
            permission_url,
            content_type='application/json'
        )
        self.assert200(response)

    def test_filter_data(self):
        """ Test filter data with filtered string """
        permission_url = url_for('auth.permission_permission_list')
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
                'created_by': 'Test_123812378171',
                'updated_by': 'Test_123812378171'
            }
        ]

        for param in params:
            temp = {"data": param}
            role_data = json.dumps(temp)

            self.client.post(
                permission_url,
                data=role_data,
                content_type='application/json'
            )

        extra_url = permission_url + '?active=1'
        permission_response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(permission_response)

        json_response = json.loads(permission_response.get_data(as_text=True))
        json_response = json_response['data']
        self.assertEqual(len(json_response), 2)

        now_time = datetime.utcnow()
        yesterday = now_time - timedelta(1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        tomorrow = now_time + timedelta(1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")

        extra__day_url = permission_url + '?created_at='+yesterday+','+tomorrow
        response = self.client.get(
            extra__day_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        json_response = json_response['data']
        self.assertEqual(len(json_response), 3)


if __name__ == "__main__":
    unittest.main()
