"""Test init."""
import json

from flask import url_for
from flask_testing import TestCase

from manage import app
from app.service.users import UserServices
from app.models import db


class BaseTest(TestCase):
    """Test dev releted test cases."""

    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self):
        """create user helper method"""
        user_data = {
            "first_name": "Test",
            "last_name": "User1",
            "email": "user1@example.com",
            "phone": "01911111114",
            "password": "123456",
            "birth_date": "1993-11-25"
        }

        user = UserServices().create(user_data)
        return user[0]['data']

    def get_user(self, user_id):
        """get_user helper method"""
        user = UserServices().get_user_details(user_id)
        return user[0]['data']

    def create_role(self):
        """create role helper method"""
        url = url_for('auth.role_role_list')
        params = {
            'name': 'test_role',
            'active': True,
            'created_by': 'test_user1',
            'updated_by': 'test_user1'
        }
        role_json = json.dumps(params)

        response = self.client.post(
            url,
            data=role_json,
            content_type='application/json'
        )
        return response.json['data']

    def assign_role_to_user(self, user_id, role_id):
        """assign role to user helper method"""
        url = url_for('auth.user-role_user_role')
        request_data = {
            "user_id": user_id,
            "role_id": role_id,
            "active": 1
        }
        request_json = json.dumps(request_data)
        response = self.client.post(
            url,
            data=request_json,
            content_type='application/json'
        )
        return response.json['data']

    def login(self):
        """login function"""
        user = self.create_user()
        role = self.create_role()
        self.assign_role_to_user(user['id'], role['id'])

        request_data = {
            "email": user['email'],
            "password": '123456',
        }
        response = UserServices().login(request_data)
        return response[0]['data']
