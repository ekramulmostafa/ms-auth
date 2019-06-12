""" Role service """
from app.service.base_service import BaseService
from app.models.role import Role, RoleSchema

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class RoleService(BaseService):
    """ Role service """
    class Meta:
        """ Meta data"""
        model = Role
        model_schema = role_schema
        models_schema = roles_schema
        # searchable = ['name']
        # sortable = ['id', '!created_at', 'updated_at']
        # filterable = ['active', 'created_at', 'updated_at']
