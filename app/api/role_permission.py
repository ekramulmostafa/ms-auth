"""API for Role Permission resource"""
# from flask import request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role_permission import RolePermissionSchema
from app.service.role_permission_service import RolePermissionService

from app.api.base import ApiResource


api = Namespace('role-permission')


logger = Logger(__name__)

# rp_schema = RolePermissionSchema()
# rps_schema = RolePermissionSchema(many=True)


@api.route('')
class RolePermissionList(ApiResource):
    """Role Permission list functionalities"""
    class Meta:
        """ Role permission meta """

        sortable = ['id', '!created_at', 'updated_at']
        filterable = ['role_id', 'permission_id', 'created_at', 'updated_at']

        service = RolePermissionService()
        allowed_methods = ['GET', 'POST']
        schema = RolePermissionSchema()
        schemas = RolePermissionSchema(many=True)


@api.route('/<uuid:uuid>')
@api.response(404, 'Role Permission not found')
class RolePermissionDetail(ApiResource):
    """ Role Permission detail functions written """
    class Meta:
        service = RolePermissionService()
        allowed_methods = ['GET', 'PUT']
        schema = RolePermissionSchema()
        schemas = RolePermissionSchema(many=True)
    # def get(self, uuid):
    #     """ GET role permission """
    #     logger.info("GET role permission")
    #
    #     role_obj = RolePermission.query.get(uuid)
    #     if role_obj is None:
    #         return {'message': 'Role Permission not found'}, 404
    #
    #     role_permission = rp_schema.dump(role_obj).data
    #
    #     return {'status': 'success', 'data': role_permission}, 200
    #
    # def put(self, uuid):
    #     """ Update role permission """
    #     logger.info("Update role permission")
    #
    #     role_obj = RolePermission.query.get(uuid)
    #     if role_obj is None:
    #         return {'message': 'Role Permission not found'}, 404
    #
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input found'}, 400
    #
    #     json_data['updated_by'] = get_current_user()
    #
    #     role_permission, errors = rp_schema.load(json_data, instance=role_obj, partial=True)
    #     if errors:
    #         logger.warning("Update role permission error", data=errors)
    #         return errors, 422
    #
    #     role_permission.save_data()
    #     result = rp_schema.dump(role_permission).data
    #     return {'status': 'success', 'data': result}, 200
