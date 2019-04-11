""" Test permission api"""
import json
import unittest

import flask_bcrypt
from flask import url_for

from app.models.users import Users
from app.models.verification_codes import VerificationCodes
from app.service.users import UsersServices
from app.test import BaseTest

user_service = UsersServices()


class UserTests(BaseTest):
    """ Test User api"""

    def test_01_get_all_users(self):
        """ test GET all user"""
        url = url_for('auth.user_user_list_api')

        user_data = {
            "first_name": "Test",
            "last_name": "User1",
            "username": "user1",
            "email": "user1@example.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25",
            "status": 1
        }

        user, status = user_service.create(user_data)
        self.assertEqual(status, 201)
        self.assertEqual(user['status'], 'success')

        response = self.client.get(url)
        self.assert200(response)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_02_filter_search_get_all_users(self):
        """ test filter search all user"""
        base_url = url_for('auth.user_user_list_api')

        user_data = {
            "first_name": "A",
            "last_name": "User1",
            "username": "user1",
            "email": "user1@example.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25",
            "status": 1
        }

        user_service.create(user_data)

        user_data['first_name'] = 'Z'
        user_data['username'] = 'user2'
        user_data['email'] = 'user2@example.com'
        user_service.create(user_data)

        response = self.client.get(base_url)
        self.assert200(response)
        response_data = json.loads(response.data.decode())

        self.assertEqual(response_data['data']['total'], 2)
        self.assertEqual(response_data['data']['offset'], 0)
        self.assertEqual(response_data['data']['limit'], 20)

        url = base_url+'?search=A'
        response = self.client.get(url)
        self.assert200(response)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['data']['total'], 1)

        url = base_url+'?active=true&sorted_by=username&order_by=desc'
        response = self.client.get(url)
        self.assert200(response)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['data']['total'], 2)
        self.assertEqual(response_data['data']['users'][0]['username'], 'user2')

        url = base_url+'?active=true&sorted_by=first_name&order_by=desc&offset=0&limit=1'
        response = self.client.get(url)
        self.assert200(response)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['data']['total'], 2)
        self.assertEqual(response_data['data']['users'][0]['first_name'], 'Z')
        self.assertEqual(len(response_data['data']['users']), 1)

    def test_03_create_user_success(self):
        """ test create user"""

        base_url = url_for('auth.user_user_list_api')

        user_data = {
            "data": {
                "first_name": "Test",
                "last_name": "User1",
                "username": "user1",
                "email": "user1@example.com",
                "phone": "01911111114",
                "password": "123456",
                "birth_date": "1993-11-25"
            }
        }

        user_data = json.dumps(user_data)
        user1_response = self.client.post(
            base_url,
            data=user_data,
            content_type='application/json'
        )
        user1_data = json.loads(user1_response.data.decode())

        self.assertEqual(user1_response.status_code, 201)
        self.assertEqual(user1_data['data']['email'], "user1@example.com")
        self.assertEqual(user1_data['data']['status'], 1)

    def test_04_create_user_failure(self):
        """ test create user"""

        base_url = url_for('auth.user_user_list_api')

        user_data = {
            "data": {
                "phone": "01911111114",
                "password": "123456",
                "birth_date": "1993-11-25"
            }
        }

        user_json_data = json.dumps(user_data)
        user_response = self.client.post(
            base_url,
            data=user_json_data,
            content_type='application/json'
        )
        user_response_data = json.loads(user_response.data.decode())

        self.assertEqual(user_response.status_code, 422)
        self.assertEqual(user_response_data['status'], "error")
        self.assertEqual(user_response_data['message']['first_name'][0],
                         'Missing data for required field.')
        self.assertEqual(user_response_data['message']['last_name'][0],
                         'Missing data for required field.')
        self.assertEqual(user_response_data['message']['email'][0],
                         'Missing data for required field.')

        user_data['data']['first_name'] = 'Test'
        user_data['data']['last_name'] = 'User1'
        user_data['data']['email'] = 'user1@example.com'

        user_json_data = json.dumps(user_data)
        user1_response = self.client.post(
            base_url,
            data=user_json_data,
            content_type='application/json'
        )

        self.assertEqual(user1_response.status_code, 201)

        user1_response = self.client.post(
            base_url,
            data=user_json_data,
            content_type='application/json'
        )
        user_response_data = json.loads(user1_response.data.decode())

        self.assertEqual(user1_response.status_code, 422)
        self.assertEqual(user_response_data['message']['email'][0],
                         'A registered user found with this email')

    def test_05_get_user_details(self):
        """ test create user"""

        user_data = {
            "first_name": "Test",
            "last_name": "User1",
            "email": "user1@example.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25",
        }
        user1 = user_service.create(user_data)[0]

        user_data['email'] = "user2@example.com"
        user2 = user_service.create(user_data)[0]

        url_user1 = url_for('auth.user_user_detail_api', uuid=user1['data']['id'])
        response_user1 = self.client.get(url_user1)
        user1_response_data = json.loads(response_user1.data.decode())
        self.assertEqual(response_user1.status_code, 200)

        url_user2 = url_for('auth.user_user_detail_api', uuid=user2['data']['id'])

        response_user2 = self.client.get(url_user2)
        user2_response_data = json.loads(response_user2.data.decode())

        self.assertEqual(response_user2.status_code, 200)

        self.assertNotEqual(user1_response_data['data']['id'],
                            user2_response_data['data']['id'])

    def test_06_user_update(self):
        """ test update user"""

        url = url_for('auth.user_user_list_api')

        user_data = {
            "data": {
                "first_name": "Test",
                "last_name": "User1",
                "username": "user1",
                "email": "user1@example.com",
                "phone": "01911111114",
                "password": "123456",
                "birth_date": "1993-11-25"
            }
        }

        user_json_data = json.dumps(user_data)
        user_response = self.client.post(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_response_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 201)

        url = url_for('auth.user_user_detail_api', uuid=user_response_data['data']['id'])
        user_data['data']['birth_date'] = "1994-11-25"
        user_json_data = json.dumps(user_data)

        user_response = self.client.put(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_updated_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 200)
        self.assertNotEqual(user_response_data['data']['birth_date'],
                            user_updated_data['data']['birth_date'])

        user_partial_data = {
            "data": {
                "first_name": "Test_Update"
            }
        }
        user_json_data = json.dumps(user_partial_data)

        user_response = self.client.put(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_updated_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response_data['data']['id'], user_updated_data['data']['id'])
        self.assertNotEqual(user_response_data['data']['first_name'],
                            user_updated_data['data']['first_name'])

        user_partial_data = {
            "data": {
                "first_name": "Test_Update"
            }
        }
        user_json_data = json.dumps(user_partial_data)

        user_response = self.client.put(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_updated_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response_data['data']['id'], user_updated_data['data']['id'])
        self.assertNotEqual(user_response_data['data']['first_name'],
                            user_updated_data['data']['first_name'])

    def test_07_user_update_failure(self):
        """test update user failure case"""

        url = url_for('auth.user_user_list_api')

        user_data = {
            "data": {
                "first_name": "Test",
                "last_name": "User1",
                "username": "user1",
                "email": "user1@example.com",
                "phone": "01911111114",
                "password": "123456",
                "birth_date": "1993-11-25"
            }
        }

        user_json_data = json.dumps(user_data)
        user_response = self.client.post(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_response_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 201)

        user_partial_data = {
            "data": {
                "email": "user2@example.com"
            }
        }
        user_json_data = json.dumps(user_partial_data)

        url = url_for('auth.user_user_detail_api', uuid=user_response_data['data']['id'])
        user_response = self.client.put(
            url,
            data=user_json_data,
            content_type='application/json'
        )
        user_updated_data = json.loads(user_response.data.decode())

        self.assertEqual(user_response.status_code, 422)
        self.assertEqual(user_updated_data['message']['email'][0],
                         'User email can not be changed')

    def test_08_user_forget_password(self):
        """test forget password case"""

        url = url_for('auth.user_user_forget_password_api')

        user_data = {
            "first_name": "Test",
            "last_name": "User1",
            "username": "user1",
            "email": "tauwab@mailinator.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25",
            "status": 1
        }

        user, status = user_service.create(user_data)
        self.assertEqual(status, 201)
        self.assertEqual(user['status'], 'success')

        request_data = {
            "data": {
                "email": "tauwab@mailinator.com"
            }
        }
        request_json_data = json.dumps(request_data)

        response = self.client.post(
            url,
            data=request_json_data,
            content_type='application/json'
        )

        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'],
                         'A password reset code has been sent to email address')

        request_data = {
            "data": {
                "phone": "01911111114"
            }
        }
        request_json_data = json.dumps(request_data)
        response = self.client.post(
            url,
            data=request_json_data,
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'],
                         'A password reset code has been sent to email address')

        request_data = {
            "data": {
                "phone": "invalid phone"
            }
        }
        request_json_data = json.dumps(request_data)
        response = self.client.post(
            url,
            data=request_json_data,
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'], 'No User found')

    def test_09_user_reset_password(self):
        """test password reset case"""

        user_data = {
            "first_name": "Test",
            "last_name": "User1",
            "username": "user1",
            "email": "tauwab@mailinator.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25",
            "status": 1
        }

        user, status = user_service.create(user_data)
        self.assertEqual(status, 201)
        self.assertEqual(user['status'], 'success')

        request_data = {
            "email": "tauwab@mailinator.com"
        }
        response, status = user_service.forget_password(request_data)
        self.assertEqual(status, 200)

        vc_obj = VerificationCodes.query.filter_by(user_id=user['data']['id'],
                                                   types=1,
                                                   status=1).first()
        code = vc_obj.code
        url = url_for('auth.user_user_reset_password_api', code=code)

        request_data = {
            "data": {
                "password": "1234567"
            }
        }
        request_json_data = json.dumps(request_data)
        response = self.client.post(
            url,
            data=request_json_data,
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], 'password updated successfully')

        updated_user = Users.query.filter_by(id=user['data']['id']).first()

        is_password_correct = flask_bcrypt.check_password_hash(updated_user.password,
                                                               request_data['data']['password'])
        self.assertTrue(is_password_correct)

        is_password_correct = flask_bcrypt.check_password_hash(updated_user.password,
                                                               user_data['password'])
        self.assertFalse(is_password_correct)

        response = self.client.post(
            url,
            data=request_json_data,
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'], 'Reset password failed')

    def test_09_user_verification(self):
        """test user verification"""
        base_url = url_for('auth.user_user_list_api')

        user_data = {
            "data": {
                "first_name": "Test",
                "last_name": "User1",
                "username": "user1",
                "email": "tauwab@mailinator.com",
                "phone": "01911111114",
                "password": "123456",
                "birth_date": "1993-11-25"
            }
        }

        user_data = json.dumps(user_data)
        user_response = self.client.post(
            base_url,
            data=user_data,
            content_type='application/json'
        )
        user_response_data = json.loads(user_response.data.decode())

        self.assertEqual(user_response.status_code, 201)
        self.assertEqual(user_response_data['data']['verified'], False)

        vc_obj = VerificationCodes.query.filter_by(user_id=user_response_data['data']['id'],
                                                   types=2,
                                                   status=1).first()

        code = vc_obj.code
        verification_url = url_for('auth.user_user_verification_api', code=code)

        user_response = self.client.get(verification_url)
        user_response_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response_data['data']['verified'], True)

        user_response = self.client.get(verification_url)
        user_response_data = json.loads(user_response.data.decode())
        self.assertEqual(user_response.status_code, 400)
        self.assertEqual(user_response_data['message'], 'user verification failed')


if __name__ == "__main__":
    unittest.main()
