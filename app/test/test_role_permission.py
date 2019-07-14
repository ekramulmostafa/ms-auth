# """Test Role"""
#
# import unittest
# import json
# from flask import url_for
# from app.test import BaseTest
#
#
# class RolePermissionTests(BaseTest):
#     """ Role Permission Test api class """
#
#     def test_insert_update_delete(self):
#         """ insert, update, delete roles permission"""
#
#         role_url = url_for('auth.role_role_list')
#         prm = {
#             'name': 'role_test',
#             'active': True,
#         }
#         role_data = json.dumps(prm)
#
#         response = self.client.post(
#             role_url,
#             data=role_data,
#             content_type='application/json'
#         )
#
#         role_id = response.json['data']['id']
#
#         permission_url = url_for('auth.permission_permission_list')
#         prm = {
#             'code': 'permission_test',
#             'name': 'permission_test',
#             'active': True
#         }
#         permission_data = json.dumps(prm)
#         response = self.client.post(
#             permission_url,
#             data=permission_data,
#             content_type='application/json'
#         )
#
#         permission_id = response.json['data']['id']
#
#         # insert role permission
#         params = {"role_id": role_id,
#                   "permission_id": permission_id,
#                   "status": "false", }
#         role_permission = json.dumps(params)
#
#         url = url_for('auth.role-permission_role_permission_list')
#
#         response = self.client.post(
#             url,
#             data=role_permission,
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json['data']['permission_id'], permission_id)
#
#         # update role permission
#         params = {
#             "status": "true",
#         }
#
#         role_permission = json.dumps(params)
#         url = url_for('auth.role-permission_role_permission_detail',
#                       uuid=response.json['data']['id'])
#
#         response = self.client.put(
#             url,
#             data=role_permission,
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['data']['status'], True)
#
#         # check readonly fields value changing
#         created_at = response.json['data']['created_at']
#         updated_at = response.json['data']['updated_at']
#         self.assertIsNotNone(updated_at)
#         self.assertNotEqual(created_at, updated_at)
#
#         url = url_for('auth.role-permission_role_permission_list')
#         response = self.client.get(url,
#                                    content_type='application/json'
#                                    )
#         self.assertEqual(response.status_code, 200)
#         self.assertGreaterEqual(len(response.json['data']), 1)
#
#
# if __name__ == "__main__":
#     unittest.main()
