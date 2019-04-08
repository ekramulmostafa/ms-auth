"""Test init."""
import json

from flask import url_for
from flask_testing import TestCase

from app.service.users import UsersServices
from manage import app
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

        user = UsersServices().create(user_data)
        return user[0]['data']

    def create_role(self):
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
        response_data = json.loads(response.data.decode())
        return response_data['data']

    def assign_role_to_user(self, user_id, role_id):

        url = url_for('auth.user_role_user_role')
        response = self.client.post(
            url,
            data=json.dumps(dict(
                user_id=user_id,
                role_id=role_id,
                active=1
            )),
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())
        return response_data['data']
