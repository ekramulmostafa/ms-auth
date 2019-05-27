""" Role service """
from app.service.base_service import BaseService


class RoleService(BaseService):
    """ Role service """
    class Meta:
        __model__ = 'Role'
