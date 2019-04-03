"""Test Role"""

import unittest
import json
from flask import url_for
from app.test import BaseTest


class RolePermissionTests(BaseTest):
    """ Role Permission Test api class """

    def test_insert_update_delete(self):
        """ insert, update, delete roles permission"""

        role_url = url_for('auth.role_role_list')
        prm = {
            'name': 'role_test',
            'active': True,
            'created_by': 'Test_12381237817',
            'updated_by': 'Test_12381237817'
        }
        role_data = json.dumps(prm)

        response = self.client.post(
            role_url,
            data=role_data,
            content_type='application/json'
        )

        json_response = json.loads(response.get_data(as_text=True))

        role_id = json_response['data']['id']

        permission_url = url_for('auth.permission_permission_list')
        prm = {
            'code': 'permission_test',
            'name': 'permission_test',
            'active': True
        }
        permission_data = json.dumps(prm)
        response = self.client.post(
            permission_url,
            data=permission_data,
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))

        permission_id = json_response['data']['id']

        # insert role permission
        params = {"role_id": role_id,
                  "permission_id": permission_id,
                  "status": "false",
                  "created_by": "1123123",
                  "updated_by": "12323122"}
        role_permission = json.dumps(params)

        url = url_for('auth.role_permission_role_permission_list')

        response = self.client.post(
            url,
            data=role_permission,
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['data']['permission_id'], permission_id)

        # update role permission
        params = {
            "status": "true",
            "created_by": "1123123",
            "updated_by": "12323122"}

        role_permission = json.dumps(params)
        url = url_for('auth.role_permission_role_permission_detail',
                      role_id=role_id,
                      permission_id=permission_id)

        response = self.client.put(
            url,
            data=role_permission,
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['data']['status'], True)

        # delete role permission

        url = url_for('auth.role_permission_role_permission_detail',
                      role_id=role_id,
                      permission_id=permission_id)

        response = self.client.delete(
            url,
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        url = url_for('auth.role_permission_role_permission_detail',
                      role_id=role_id,
                      permission_id=permission_id)
        response = self.client.get(
            url,
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
