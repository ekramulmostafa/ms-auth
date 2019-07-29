""" Role Permission service """
from app.service.base_service import BaseService
from app.models.role_permission import RolePermission


class RolePermissionService(BaseService):
    """ Role service """
    class Meta:
        """ Meta data"""
        model = RolePermission
