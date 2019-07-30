"""Test Role"""

from datetime import datetime, timedelta
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

        response = self.client.put(
            url,
            data=permission_data,
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
                'created_by': 'Test_123812378174',
                'updated_by': 'Test_123812378174'
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
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))['data']
        self.assertEqual(len(json_response), 2)

        today = datetime.utcnow()
        yesterday = today - timedelta(1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        tomorrow = today + timedelta(1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")

        extra_url = permission_url + '?created_at='+yesterday+','+tomorrow
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))['data']
        self.assertEqual(len(json_response), 3)


if __name__ == "__main__":
    unittest.main()
