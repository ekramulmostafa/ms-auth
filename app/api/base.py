""" API base class """

from flask_restplus import Resource
from flask import request, session

from app.utils.decorator import token_required


class BaseResource(Resource):
    """Resource base class"""
    __abstract__ = True

    class Meta:
        """Meta class"""
        service = None

    def get(self, uuid=None):
        """base get"""
        pass

    def post(self):
        """base post"""
        pass

    def put(self, uuid=None):
        """base put"""
        pass


class DefaultResource(BaseResource):
    """Resource for generic """

    def post(self):
        """post for generic"""
        service = self.Meta.service
        data = request.get_json(force=True)
        return service.create(data['data'])

    def get(self, uuid=None):
        """ get for details """
        service = self.Meta.service
        if uuid:
            return service.fetch(uuid)
        else:
            return service.fetch()

    def put(self, uuid=None):
        """put for update"""
        service = self.Meta.service
        data = request.json
        return service.update(data['data'], uuid)


class ProtectedResource(BaseResource):
    """Resource where token is required """

    @token_required
    def post(self):
        """post where token is required"""
        service = self.Meta.service
        data = request.get_json(force=True)
        user = session['current_user']
        data['data']['created_by'] = user['id']
        data['data']['updated_by'] = user['id']
        return service.create(data['data'])

    @token_required
    def get(self, uuid=None):
        """ get where token is required"""
        service = self.Meta.service
        if uuid:
            return service.fetch(uuid)
        else:
            return service.fetch()

    @token_required
    def put(self, uuid=None):
        """put where token is required"""
        service = self.Meta.service
        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']
        return service.update(data['data'], uuid)
