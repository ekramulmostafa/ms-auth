""" API base class """

from flask_restplus import Resource
from flask import request


class BaseResource(Resource):
    """Resource base class"""
    __abstract__ = True


class ResourceAll(BaseResource):
    """Resource for generic """

    class Meta:
        """Meta class"""
        service = None

    def get(self):
        """get for generic"""
        service = self.Meta.service
        users = service.get()
        return users

    def post(self):
        """post for generic"""
        service = self.Meta.service
        json_data = request.get_json(force=True)
        return service.post(json_data['data'])


class ResourceDetails(BaseResource):
    """ resource for details """

    class Meta:
        """Meta class"""
        service = None

    def get(self, value):
        """ get for details """
        service = self.Meta.service
        return service.get(value)
