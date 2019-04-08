"""test current user"""
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
