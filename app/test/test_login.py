import json

from flask import url_for

from app.test import BaseTest

from app.service.users import UsersServices

user_service = UsersServices()


class UserLoginTests(BaseTest):
    """ Test User api"""

    def test_01_login(self):
        """ test Login user"""
        user = self.create_user()
        role = self.create_role()
        self.assign_role_to_user(user['id'], role['id'])

        login_url = url_for('auth.user_user_login_api')

        login_data = {
            "data": {
                "email": user['email'],
                "password": "123456"
            }
        }

        user_data = json.dumps(login_data)
        response = self.client.post(
            login_url,
            data=user_data,
            content_type='application/json'
        )

        self.assert200(response)
        self.assertEqual(response.json['status'], 'success')

        login_data = {
            "data": {
                "phone": user['phone'],
                "password": "123456"
            }
        }

        user_data = json.dumps(login_data)
        response = self.client.post(
            login_url,
            data=user_data,
            content_type='application/json'
        )

        self.assert200(response)
        self.assertEqual(response.json['status'], 'success')

        login_data = {
            "data": {
                "phone": user['phone'],
                "password": "InvalidPassword"
            }
        }

        user_data = json.dumps(login_data)
        response = self.client.post(
            login_url,
            data=user_data,
            content_type='application/json'
        )

        self.assert400(response)
        self.assertEqual(response.json['status'], 'error')
