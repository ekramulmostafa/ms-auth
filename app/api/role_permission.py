"""API for Role Permission resource"""
from flask import request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role_permission import RolePermission, RolePermissionSchema
from app.utils.get_current_user import get_current_user
api = Namespace('role-permission')


logger = Logger(__name__)

rp_schema = RolePermissionSchema()
rps_schema = RolePermissionSchema(many=True)


@api.route('')
class RolePermissionList(Resource):
    """Role Permission list functionalities"""

    def get(self):
        """ get all role permissions """
        rp = RolePermission.query.all()
        results = rps_schema.dump(rp).data
        return {'status': 'success', 'data': results}, 200

    def post(self):
        """Insert a role permissions"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input Role or Permission provided'}, 400
        logger.info("Insert a role permission", data=json_data)

        json_data['created_by'] = get_current_user()
        json_data['updated_by'] = get_current_user()

        role_permission, errors = rp_schema.load(json_data, partial=True)

        if errors:
            logger.warning("Insert role permission error", data=errors)
            return errors, 422
        role_permission.save_data()

        result = rp_schema.dump(role_permission).data
        return {'status': 'success', 'data': result}, 201


@api.route('/<uuid:uuid>')
@api.response(404, 'Role Permission not found')
class RolePermissionDetail(Resource):
    """Role Permission detail funtions written"""

    def get(self, uuid):
        """ GET role permission """
        logger.info("GET role permission")

        role_obj = RolePermission.query.get(uuid)
        if role_obj is None:
            return {'message': 'Role Permission not found'}, 404

        role_permission = rp_schema.dump(role_obj).data

        return {'status': 'success', 'data': role_permission}, 200

    def put(self, uuid):
        """ Update role permission """
        logger.info("Update role permission")

        role_obj = RolePermission.query.get(uuid)
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

        role_permission.save_data()
        result = rp_schema.dump(role_permission).data
        return {'status': 'success', 'data': result}, 200
