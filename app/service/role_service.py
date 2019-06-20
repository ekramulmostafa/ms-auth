""" Role service """
from app.service.base_service import BaseService
from app.models.role import Role


class RoleService(BaseService):
    """ Role service """
    class Meta:
        """ Meta data"""
        model = Role
