""" API base class """

from flask_restplus import Resource
from flask import request


class BaseResource(Resource):
    """Resource base class"""
    __abstract__ = True

    class Meta:
        """Meta class"""
        service = None

    def get(self, uuid=None):
        pass

    def post(self):
        pass

    def put(self, uuid=None):
        pass


class DefaultResource(BaseResource):
    """Resource for generic """

    def post(self):
        """post for generic"""
        service = self.Meta.service
        data = request.get_json(force=True)
        return service.post(data['data'])

    def get(self, uuid=None):
        """ get for details """
        service = self.Meta.service
        if uuid:
            return service.get(uuid)
        else:
            return service.get()

    def put(self, uuid=None):
        service = self.Meta.service
        data = request.json
        return service.put(data['data'], uuid)
