""" Role service """
from app.service.base_service import BaseService
from app.models.role import Role


class RoleService(BaseService):
    """ Role service """
    class Meta:
        __model__ = Role
        __searchable__ = ['name']
        __sortable__ = ['id', '!created_at', 'updated_at']
