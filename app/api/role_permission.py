"""API for Role Permission resource"""

from flask_restplus import Namespace
from app.logging import Logger
from app.models.role_permission import RolePermissionSchema
from app.service.role_permission_service import RolePermissionService

from app.api.base import ApiResource


api = Namespace('role-permission')


logger = Logger(__name__)


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
        """ Role permission detail meta """
        service = RolePermissionService()
        allowed_methods = ['GET', 'PUT']
        schema = RolePermissionSchema()
        schemas = RolePermissionSchema(many=True)
