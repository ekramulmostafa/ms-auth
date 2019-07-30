"""Test Role"""

from datetime import datetime, timedelta
import unittest
import json
from flask import url_for
from app.test import BaseTest


class RoleTests(BaseTest):
    """ Role Test api class """

    def test_insert_update(self):
        """ insert roles then update and then get the updated role and insert multiple roles """

        url = url_for('auth.role_role_list')

        params = {
            'data': {
                'name': 'test_role',
                'active': True,
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        }
        role_data = json.dumps(params)

        response = self.client.post(
            url,
            data=role_data,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))

        put_id = json_response['data']['id']

        self.assertEqual(response.status_code, 201)

        params = {
            'data': {
                'name': 'test_role_update',
                'active': False,
                'updated_by': 'Test_1238123'
            }
        }

        role_data = json.dumps(params)

        url = url_for('auth.role_role_detail', uuid=put_id)

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

        self.assertEqual(json_response['name'], 'test_role_update')

        # check readonly fields value changing
        self.assertIsNotNone(json_response['updated_at'])
        self.assertNotEqual(json_response['created_at'], json_response['updated_at'])

    def test_get_all_roles(self):
        """ Get all roles and also filtered roles """
        url = url_for('auth.role_role_list')
        params = [
            {
                'name': 'test_role2',
                'active': True,
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_role3',
                'active': False,
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_role4',
                'active': True,
                'created_by': 'Test_123812378173',
                'updated_by': 'Test_123812378173'
            }
        ]

        for param in params:
            role_data = json.dumps({"data": param})

            self.client.post(
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
        url = url_for('auth.role_role_list')
        params = [
            {
                'name': 'test_role2',
                'active': True,
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_role3',
                'active': False,
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            },
            {
                'name': 'test_role4',
                'active': True,
                'created_by': 'Test_123812378172',
                'updated_by': 'Test_123812378172'
            }
        ]

        for param in params:
            data = {"data": param}
            role_data = json.dumps(data)

            self.client.post(
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

        today = datetime.utcnow()
        yesterday = today - timedelta(1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        tomorrow = today + timedelta(1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")

        extra_url = url + '?created_at=' + yesterday + ',' + tomorrow
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))['data']
        self.assertEqual(len(json_response), 3)


if __name__ == "__main__":
    unittest.main()
