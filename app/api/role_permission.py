"""API for Role resource"""
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role_permission import RolePermission, RolePermissionSchema
from app.models.role import Role
from app.models.permission import Permission

api = Namespace('role_permission')
role_permission_schema = RolePermissionSchema()
roles_Permissions_schema = RolePermissionSchema(many=True)


logger = Logger(__name__)


@api.route('')
class RolePermissionList(Resource):
    """Role list functionalities"""

    def get(self):
        """Get all role"""

        logger.info("Get all role")
        roles = RolePermission.query.all()

        result = roles_Permissions_schema.dump(roles)
        return jsonify(result.data)

    def post(self):
        """Insert a role"""

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        logger.info("Insert a role", data=json_data)

        print('role_permission_start')
        print(json_data)
        role = Role.query.get(json_data['role_id'])
        # print(role.name)
        permission = Permission.query.get(json_data['permission_id'])
        # print(permission.name)
        # RolePermission.save(role, permission)
        role.role_permission.append(permission)

        print('role_permission_end')
        # Validate and deserialize input
        # role_permission, errors = role_permission_schema.load(json_data)
        # if errors:
        #     logger.warning("Insert role error", data=errors)
        #     return errors, 422

        # role.save()
        # result = role_schema.dump(role).data
        # return {'status': 'success', 'data': result}, 201
