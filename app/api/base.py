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

    def post(self):
        """post for generic"""
        meth = getattr(self.Meta, 'methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.get_json(force=True)
        return self.Meta.service.create(data['data'])

    def get(self, uuid=None):
        """ get for details """
        meth = getattr(self.Meta, 'methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        if uuid:
            return self.Meta.service.fetch(uuid)
        return self.Meta.service.fetch()

    def put(self, uuid=None):
        """put for update"""
        meth = getattr(self.Meta, 'methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.json
        return self.Meta.service.update(data['data'], uuid)


class ProtectedResource(BaseResource):
    """Resource where token is required """

    @token_required
    def post(self):
        """post where token is required"""
        meth = getattr(self.Meta, 'methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.get_json(force=True)
        user = session['current_user']
        data['data']['created_by'] = user['id']
        data['data']['updated_by'] = user['id']
        return self.Meta.service.create(data['data'])

    @token_required
    def get(self, uuid=None):
        """ get where token is required"""

        meth = getattr(self.Meta, 'methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        if uuid:
            return self.Meta.service.fetch(uuid)
        return self.Meta.service.fetch()

    @token_required
    def put(self, uuid=None):
        """put where token is required"""
        meth = getattr(self.Meta, 'methods', None)
        if meth and (not meth.__contains__(request.method)):
            abort(405)

        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']
        return self.Meta.service.update(data['data'], uuid)
