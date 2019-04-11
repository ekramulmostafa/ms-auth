"""Test Role"""

import unittest
import json
from datetime import datetime, timedelta
from flask import url_for
from app.test import BaseTest


class RoleTests(BaseTest):
    """ Role Test api class """

    def test_insert_update(self):
        """ insert roles then update and then get the updated role and insert multiple roles """

        url = url_for('auth.role_role_list')

        params = {
            'name': 'test_role',
            'active': True,
            'created_by': 'Test_12381237817',
            'updated_by': 'Test_12381237817'
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
            'name': 'test_role_update',
            'active': False,
            'updated_by': 'Test_1238123'
        }
        role_data = json.dumps(params)

        url = url_for('auth.role_role_detail', uuid=put_id)

        response = self.client.put(
            url,
            data=role_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            url,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))

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
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps(param)

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

    def test_order_by_method(self):
        """ Get all roles and order by filter test """
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
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps(param)

            response = self.client.post(
                url,
                data=role_data,
                content_type='application/json'
            )

        # Order by created_at desc
        extra_url = url + '?order_by_field=created_at&order_by=desc'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response[0]['name'], params[-1]['name'])

        # Order by created_at desc
        extra_url = url + '?order_by_field=created_at'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response[0]['name'], params[0]['name'])

        # Order by created_at desc
        extra_url = url + '?order_by_field=updated_at&order_by=desc'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response[0]['name'], params[-1]['name'])

        # Order by created_at desc
        extra_url = url + '?order_by_field=updated_at'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response[0]['name'], params[0]['name'])

        # Limit and offset check
        extra_url = url + '?order_by_field=created_at&order_by=desc&limit=1&offset=1'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        # print(len(json_response))
        self.assertEqual(len(json_response), 1)

    def test_query_string(self):
        """ Get all roles and query string test """
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
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps(param)

            response = self.client.post(
                url,
                data=role_data,
                content_type='application/json'
            )
        # Search
        extra_url = url + '?q=test_role2'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        # print(json_response)
        self.assertEqual(json_response[0]['name'], 'test_role2')

        # Search Boolean
        extra_url = url + '?q=true'
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        # print(json_response)
        self.assertEqual(len(json_response), 2)

    def test_date_time_query(self):
        """ Get all roles and Datetime test """

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
                'created_by': 'Test_12381237817',
                'updated_by': 'Test_12381237817'
            }
        ]

        for param in params:
            role_data = json.dumps(param)

            response = self.client.post(
                url,
                data=role_data,
                content_type='application/json'
            )
        # Search Datewise
        current_date = datetime.now()
        next_date = current_date + timedelta(days=1)
        extra_url = url + '?datefrom=' + current_date.strftime("%Y-%m-%d")
        extra_url += '&dateto='+next_date.strftime("%Y-%m-%d")
        response = self.client.get(
            extra_url,
            content_type='application/json'
        )
        self.assert200(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertGreaterEqual(len(json_response), 1)

        # Get Single content not found
        url = url_for('auth.role_role_detail', uuid=123123)

        response = self.client.get(
            url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
