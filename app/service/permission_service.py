""" Permission service """
from app.service.base_service import BaseService
from app.models.permission import Permission


class PermissionService(BaseService):
    """ Permission service """
    class Meta:
        """ Permission Meta data"""
        model = Permission
