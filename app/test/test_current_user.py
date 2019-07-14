# """test current user"""
# import json
#
# from flask import url_for
#
# from app.test import BaseTest
# from app.utils.utils import decode_auth_token
#
#
# class CurrentUserTests(BaseTest):
#     """ Test Current User api"""
#
#     def test_01_get_current_user(self):
#         """ Test Current User GET api"""
#         url = url_for('auth.user_current_user_api')
#         login_reponse = self.login()
#         token = 'Bearer {0}'.format(login_reponse['token'])
#         user_id = decode_auth_token(login_reponse['token'])['data']['sub']
#         headers = {
#             'Authorization': token
#         }
#         response = self.client.get(url, headers=headers)
#         json_response = response.json
#         self.assert200(response)
#         self.assertEqual(json_response['data']['id'], user_id)
#
#         response = self.client.get(url)
#         self.assert401(response)
#         json_response = response.json
#         self.assertEqual(json_response['message'], 'no authorization token found')
#
#         headers = {
#             'Authorization': login_reponse['token']
#         }
#         response = self.client.get(url, headers=headers)
#         self.assert401(response)
#         json_response = response.json
#         self.assertEqual(json_response['message'], 'Invalid Bearer token')
#
#         headers = {
#             'Authorization': 'Bearer invalidToken'
#         }
#         response = self.client.get(url, headers=headers)
#         self.assert401(response)
#         json_response = response.json
#         self.assertEqual(json_response['message'], 'invalid token')
#
#         headers = {
#             'Authorization': 'Bearer'
#         }
#         response = self.client.get(url, headers=headers)
#         self.assert401(response)
#         json_response = response.json
#         self.assertEqual(json_response['message'], 'Invalid Bearer token')
#
#     def test_02_current_user_update(self):
#         """test current user update api"""
#         login_reponse = self.login()
#         token = 'Bearer {0}'.format(login_reponse['token'])
#         user_id = decode_auth_token(login_reponse['token'])['data']['sub']
#         current_user = self.get_user(user_id)
#
#         user_partial_data = {
#             "data": {
#                 "first_name": "Current_user"
#             }
#         }
#         user_json_data = json.dumps(user_partial_data)
#
#         update_url = url_for('auth.user_current_user_api')
#         headers = {
#             'Authorization': token
#         }
#         user_response = self.client.put(
#             update_url,
#             data=user_json_data,
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assert200(user_response)
#         json_response = user_response.json
#         self.assertNotEqual(json_response['data']['first_name'], current_user['first_name'])
#         self.assertEqual(json_response['data']['first_name'], 'Current_user')
#         self.assertEqual(json_response['data']['id'], current_user['id'])
#
#     def test_03_current_user_password_update(self):
#         """test current user update api"""
#         login_reponse = self.login()
#         token = 'Bearer {0}'.format(login_reponse['token'])
#         user_id = decode_auth_token(login_reponse['token'])['data']['sub']
#         current_user = self.get_user(user_id)
#
#         user_password_data = {
#             "data": {
#                 "current_password": "123456",
#                 "new_password": "1234567"
#             }
#         }
#         user_json_data = json.dumps(user_password_data)
#
#         update_url = url_for('auth.user_current_user_update_password_api')
#         headers = {
#             'Authorization': token
#         }
#         user_response = self.client.put(
#             update_url,
#             data=user_json_data,
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assert200(user_response)
#         json_response = user_response.json
#         self.assertEqual(json_response['message'], 'password updated successfully')
#         self.assertEqual(current_user['status'], 1)
#
#         user_password_data = {
#             "data": {
#                 "current_password": "123456",
#                 "new_password": "1234567"
#             }
#         }
#         user_json_data = json.dumps(user_password_data)
#         user_response = self.client.put(
#             update_url,
#             data=user_json_data,
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assert400(user_response)
#         json_response = user_response.json
#         self.assertEqual(json_response['message'], 'Incorrect password')
#
#         user_password_data = {
#             "data": {
#                 "current_password": "1234567",
#                 "new_password": "123456",
#                 "status": 2,
#                 "first_name": "test_user_new"
#             }
#         }
#         user_json_data = json.dumps(user_password_data)
#         user_response = self.client.put(
#             update_url,
#             data=user_json_data,
#             headers=headers,
#             content_type='application/json'
#         )
#         self.assert200(user_response)
#         current_user = self.get_user(user_id)
#         self.assertEqual(current_user['status'], 1)
#         self.assertNotEqual(current_user['first_name'], 'test_user_new')
