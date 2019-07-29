"""API for Role resource"""

from flask_restplus import Namespace

from app.api.base import ApiResource
from app.logging import Logger
from app.models.role import RoleSchema

from app.service.role_service import RoleService


api = Namespace('role')
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

logger = Logger(__name__)


@api.route('/')
class RoleList(ApiResource):
    """Test Base functionality"""

    class Meta:
        """meta class"""

        sortable = ['id', '!created_at', 'updated_at']
        filterable = ['active', 'created_at', 'updated_at']

        service = RoleService()
        allowed_methods = ['GET', 'POST']
        schema = RoleSchema()
        schemas = RoleSchema(many=True)


@api.route('/<uuid:uuid>/')
class RoleDetail(ApiResource):
    """ Test Base details functionality """
    class Meta:
        """ meta class """
        service = RoleService()
        allowed_methods = ['GET', 'PUT']
        schema = RoleSchema()
        schemas = RoleSchema(many=True)
