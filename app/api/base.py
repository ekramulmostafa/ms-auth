""" API base class """

from flask_restplus import Resource, abort
from flask import request, session

from app.utils.decorator import token_required


class BaseResource(Resource):
    """Resource base class"""
    __abstract__ = True

    class Meta:
        """Meta class"""
        service = None
        methods = None

    def get(self, uuid=None):
        """base get"""

    def post(self):
        """base post"""

    def put(self, uuid=None):
        """base put"""


class DefaultResource(BaseResource):
    """Resource for generic """

    def __init_subclass__(cls):
        cls.meta_methods = getattr(cls.Meta, 'methods', None)
        cls.meta_services = getattr(cls.Meta, 'service', None)

    def post(self):
        """post for generic"""
        if request.method not in self.meta_methods:
            abort(405)
        data = request.get_json(force=True)
        return self.meta_services.create(data['data'])

    def get(self, uuid=None):
        """ get for details """
        if request.method not in self.meta_methods:
            abort(405)
        if uuid:
            return self.meta_services.fetch(uuid)
        return self.meta_services.fetch()

    def put(self, uuid=None):
        """put for update"""
        if request.method not in self.meta_methods:
            abort(405)
        data = request.json
        return self.meta_services.update(data['data'], uuid)


class ProtectedResource(BaseResource):
    """Resource where token is required """

    @token_required
    def post(self):
        """post where token is required"""
        if request.method not in self.meta_methods:
            abort(405)
        service = self.Meta.service
        data = request.get_json(force=True)
        user = session['current_user']
        data['data']['created_by'] = user['id']
        data['data']['updated_by'] = user['id']
        return service.create(data['data'])

    @token_required
    def get(self, uuid=None):
        """ get where token is required"""
        if request.method not in self.meta_methods:
            abort(405)
        service = self.Meta.service
        if uuid:
            return service.fetch(uuid)
        return service.fetch()

    @token_required
    def put(self, uuid=None):
        """put where token is required"""
        if request.method not in self.meta_methods:
            abort(405)
        service = self.Meta.service
        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']
        return service.update(data['data'], uuid)
