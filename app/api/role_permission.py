"""API for Role Permission resource"""
from flask import request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role_permission import RolePermission, RolePermissionSchema
from app.utils.get_current_user import get_current_user
# from pprint import pprint
api = Namespace('role_permission')


logger = Logger(__name__)

# role permission schema
rp_schema = RolePermissionSchema()
rps_schema = RolePermissionSchema(many=True)


@api.route('')
class RolePermissionList(Resource):
    """Role Permission list functionalities"""

    def post(self):
        """Insert a role permissions"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input Role or Permission provided'}, 400
        logger.info("Insert a role permission", data=json_data)

        # role = Role.query.get(json_data['role_id'])
        # permission = Permission.query.get(json_data['permission_id'])
        # role.save_role_permission(permission)
        json_data['created_by'] = get_current_user()
        json_data['updated_by'] = get_current_user()

        role_permission, errors = rp_schema.load(json_data, partial=True)

        if errors:
            logger.warning("Insert role permission error", data=errors)
            return errors, 422
        # print(role_permission.role_id)
        role_permission.save_data()

        result = rp_schema.dump(role_permission).data
        return {'status': 'success', 'data': result}, 201


@api.route('/<uuid:role_id>/<uuid:permission_id>')
@api.response(404, 'Role Permission not found')
class RolePermissionDetail(Resource):
    """Role Permission detail funtions written"""

    def get(self, role_id, permission_id):
        """ GET role permission """
        logger.info("GET role permission")

        role_obj = RolePermission.get_by_role_permission(role_id, permission_id)
        if role_obj is None:
            return {'message': 'Role Permission not found'}, 404

        role_permission, errors = rp_schema.dump(role_obj).data
        if errors:
            logger.warning("Get role permission error", data=errors)
            return errors, 422

        return {'status': 'success', 'data': role_permission}, 200

    def put(self, role_id, permission_id):
        """ Update role permission """
        logger.info("Update role permission")

        role_obj = RolePermission.get_by_role_permission(role_id, permission_id)
        if role_obj is None:
            return {'message': 'Role Permission not found'}, 404

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input found'}, 400

        json_data['updated_by'] = get_current_user()

        role_permission, errors = rp_schema.load(json_data, instance=role_obj, partial=True)
        if errors:
            logger.warning("Update role permission error", data=errors)
            return errors, 422
        # print(role)
        role_permission.save_data()
        result = rp_schema.dump(role_permission).data
        return {'status': 'success', 'data': result}, 200
