""" API base class """

from flask_restplus import Resource
from flask import request


class BaseResource(Resource):
    """Resource base class"""
    __abstract__ = True


class ResourceAll(BaseResource):
    """Resource for generic """
    def get(self):
        """get for generic"""
        print("GET")

    def post(self):
        """post for generic"""
        data = request.json
        print(data)


class ResourceDetails(BaseResource):
    """ resource for details """

    class Meta:
        """Meta class"""
        service = None

    def get(self, value):
        """ get for details """
        service = self.Meta.service
        return service.get(value)
