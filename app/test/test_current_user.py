"""test current user"""
import json

from flask import url_for

from app.test import BaseTest


class CurrentUserTests(BaseTest):
    """ Test Current User api"""

    def test_01_get_current_user(self):
        """ Test Current User GET api"""
        url = url_for('auth.user_current_user_api')
        login_reponse = self.login()
        token = 'Bearer {0}'.format(login_reponse['token'])
        user_id = login_reponse['user_id']
        headers = {
            'Authorization': token
        }
        response = self.client.get(url, headers=headers)
        json_response = response.json
        self.assert200(response)
        self.assertEqual(json_response['data']['id'], user_id)

        response = self.client.get(url)
        self.assert401(response)
        json_response = response.json
        self.assertEqual(json_response['message'], 'no authorization token found')

        headers = {
            'Authorization': login_reponse['token']
        }
        response = self.client.get(url, headers=headers)
        self.assert401(response)
        json_response = response.json
        self.assertEqual(json_response['message'], 'Invalid Bearer token')

        headers = {
            'Authorization': 'Bearer invalidToken'
        }
        response = self.client.get(url, headers=headers)
        self.assert401(response)
        json_response = response.json
        self.assertEqual(json_response['message'], 'invalid token')

        headers = {
            'Authorization': 'Bearer'
        }
        response = self.client.get(url, headers=headers)
        self.assert401(response)
        json_response = response.json
        self.assertEqual(json_response['message'], 'Invalid Bearer token')

    def test_02_current_user_update(self):
        """test current user update api"""
        login_reponse = self.login()
        token = 'Bearer {0}'.format(login_reponse['token'])
        current_user = self.get_user(login_reponse['user_id'])

        user_partial_data = {
            "data": {
                "first_name": "Current_user"
            }
        }
        user_json_data = json.dumps(user_partial_data)

        update_url = url_for('auth.user_current_user_api')
        headers = {
            'Authorization': token
        }
        user_response = self.client.put(
            update_url,
            data=user_json_data,
            headers=headers,
            content_type='application/json'
        )
        self.assert200(user_response)
        json_response = user_response.json
        self.assertNotEqual(json_response['data']['first_name'], current_user['first_name'])
        self.assertEqual(json_response['data']['first_name'], 'Current_user')
        self.assertEqual(json_response['data']['id'], current_user['id'])
