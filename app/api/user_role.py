""" User Role """
from flask import request
from flask_restplus import Resource, Namespace
# from app.models.users import Users
from app.models.user_role import UserRole as UserRoles
# from app.models.role import Role
from app.models.role import RoleSchema
from app.models.user_role import UserRoleSchema

api = Namespace("user-role")
role_schema = RoleSchema()
user_role_schema = UserRoleSchema()
user_roles_schema = UserRoleSchema(many=True)


@api.route('')
class UserRole(Resource):
    """ No method for get """

    def post(self):
        """ Add role to user """
        data = request.get_json(force=True)
        result_data, error = user_role_schema.load(data)
        if error:
            return error, 422
        result_data.save()
        user_role = user_role_schema.dump(result_data).data
        return {'status': 'success', 'data': user_role}, 200

    def put(self):
        """ Update active and inactive role for users """
        data = request.get_json(force=True)
        user_roles_obj = UserRoles.get_by_uid_rid(self, data['user_id'], data['role_id'])
        result_data, error = user_role_schema.load(data, instance=user_roles_obj, partial=True)
        if error:
            return error, 400
        result_data.save()
        result = user_role_schema.dump(result_data).data
        return {'status': 'success', 'data': result}, 200


@api.route('/<uuid:uuid>/')
class UserRoleDetail(Resource):
    """ Class user role """

    def get(self, uuid):
        """ Get user role """
        user_role = UserRoles.query.get(uuid)
        data = user_role_schema.dump(user_role).data
        return {'status': 'success', 'data': data}, 200

    def put(self, uuid):
        """ Edit role of user """
        data = request.get_json(force=True)
        if data is None:
            return {'status': 'failed', 'message': 'No data is found'}, 400
        user_role = UserRoles.query.get(uuid)
        if user_role is None:
            return {'status': 'failed', 'message': 'cannot find the uuid'}, 400
        user_role_data, error = user_role_schema.load(data, instance=user_role)
        if error:
            return error
        result = user_role_schema.dump(user_role_data).data
        return {'status': 'success', 'data': result}, 200
