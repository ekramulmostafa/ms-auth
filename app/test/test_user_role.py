""" test user role """
import json
from flask import url_for
from app.test import BaseTest
from app.models.user_role import UserRole, UserRoleSchema
from app.models.role import Role, RoleSchema
from app.models.users import Users
from app.serializers.users import UsersModelSchema


class TestUserRole(BaseTest):
    """insert data which will initially add  """

    def setUp(self):
        """ set up """
        super().setUp()
        # initial role to set
        role = {
            "name": "justrole",
            "active": 1,
            "created_by": "dsadsd",
            "updated_by": "sadsad"
        }
        role_schema = RoleSchema()
        result, error = role_schema.load(role)
        if error:
            print(error)
        data = result.save()
        data_json = role_schema.dump(result).data
        role_id = data_json['id']
        print(data_json)

        # initial data to set
        user_data = {
            "first_name": "SomeF",
            "last_name": "SomeL",
            "username": "user1some",
            "email": "some@example.com",
            "phone": "01911111314",
            "password": "12345678",
            "birth_date": "2003-11-25",
            "status": 1
        }
        user_schema = UsersModelSchema()
        user_result, error = user_schema.load(user_data)
        if error:
            print(error)
        result = user_result.save()
        result_data = user_schema.dump(user_result).data
        user_id = result_data['id']
        print(result_data)

        # user role data
        user_role = {
            'user_id': user_id,
            'role_id': role_id,
            'active': 1
        }
        user_schema = UserRoleSchema()
        result, error = user_schema.load(user_role)
        data = result.save()
        print(user_schema.dump(data))

    def test_get_user_role_by_uuid(self):
        """ get user_role by uuid """

        user_role = UserRole.query.all()
        print(user_role[0].id)
        print('user role test .... is ')
        print(user_role[0].id)
        url = url_for('auth.user_role_user_role_detail', uuid=user_role[0].id)
        response = self.client.get(
            url
        )
        self.assert200(response)

    def test_put_user_role_by_uuid(self):
        """ put user role to user table"""

        user_role = UserRole.query.all()
        user = Users.query.all()
        user_schema = UsersModelSchema()
        user_data = user_schema.dump(user[0]).data
        role = Role.query.all()
        role_schema = RoleSchema()
        role_data = role_schema.dump(role[0]).data
        url = url_for('auth.user_role_user_role_detail', uuid=user_role[0].id)
        response = self.client.put(
            url,
            data=json.dumps(dict(
                user_id=user_data['id'],
                role_id=role_data['id'],
                active=1,
            )),
            content_type='application/json'
        )
        self.assert200(response, message=None)

    def save_role(self):
        """ add another role """
        role = {
            "name": "secondrole",
            "active": 1,
            "created_by": "dsadsd",
            "updated_by": "sadsad"
        }
        role_schema = RoleSchema()
        result, error = role_schema.load(role)
        if error:
            print(error)
        result.save()
        data_json = role_schema.dump(result).data
        role_id = data_json['id']
        return role_id

    def save_user(self):
        """ save user """
        user_data = {
            "first_name": "SomeAND",
            "last_name": "SomeLALL",
            "username": "user1some",
            "email": "some1@example.com",
            "phone": "01911111316",
            "password": "12345678",
            "birth_date": "2003-11-25",
            "status": 1
        }
        user_schema = UsersModelSchema()
        user_result, error = user_schema.load(user_data)
        if error:
            print(error)
        user_result.save()
        result_data = user_schema.dump(user_result).data
        user_id = result_data['id']
        return user_id

    def test_add_user_role(self):
        """ add user role to user table """
        role_id = self.save_role()
        user_id = self.save_user()
        role = Role.query.all()
        user = Users.query.all()
        role_schema = RoleSchema()
        user_schema = UsersModelSchema()
        json_role = role_schema.dump(role[1]).data
        role_id = json_role['id']

        json_user = user_schema.dump(user[1]).data
        user_id = json_user['id']

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
        self.assert200(response)

    def test_edit_user_role(self):
        """ edit user role """
        user = Users.query.all()
        role = Role.query.all()
        user_role = UserRole.query.all()
        role_schema = RoleSchema()
        user_schema = UsersModelSchema()
        json_role = role_schema.dump(role[0]).data
        role_id = json_role['id']
        json_user = user_schema.dump(user[0]).data
        user_id = json_user['id']
        url = url_for('auth.user_role_user_role', uuid=user_role[0].id)
        response = self.client.put(
            url,
            data=json.dumps(dict(
                user_id=user_id,
                role_id=role_id,
                active=0

            )),
            content_type='application/json'
        )
        self.assert200(response)
