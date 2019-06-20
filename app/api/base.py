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
        allowed_methods = None

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
        meth = getattr(self.Meta, 'allowed_methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.get_json(force=True)
        return self.Meta.service.create(data['data'])

    def get(self, uuid=None):
        """ get for details """
        meth = getattr(self.Meta, 'allowed_methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        if uuid:
            return self.Meta.service.fetch(uuid)
        return self.Meta.service.fetch()

    def put(self, uuid=None):
        """put for update"""
        meth = getattr(self.Meta, 'allowed_methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.json
        return self.Meta.service.update(data['data'], uuid)


class ProtectedResource(BaseResource):
    """Resource where token is required """

    @token_required
    def post(self):
        """post where token is required"""
        meth = getattr(self.Meta, 'allowed_methods', None)
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

        meth = getattr(self.Meta, 'allowed_methods', None)
        if meth and not meth.__contains__(request.method):
            abort(405)

        if uuid:
            return self.Meta.service.fetch(uuid)
        return self.Meta.service.fetch()

    @token_required
    def put(self, uuid=None):
        """put where token is required"""
        meth = getattr(self.Meta, 'allowed_methods', None)
        if meth and (not meth.__contains__(request.method)):
            abort(405)

        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']
        return self.Meta.service.update(data['data'], uuid)


class CreateApiView(Resource):
    """
    create api view
    """
    def post(self):
        """post for generic"""
        meth = getattr(self.Meta, 'allowed_methods', None)
        schema = getattr(self.Meta, 'schema', None)
        service = self.Meta.service

        if meth and not meth.__contains__(request.method):
            abort(405)

        data = request.json
        result_data, errors = schema.load(data['data'])
        if errors:
            return {'status': 'error', 'data': {}, 'message': errors}, 422

        result_data = service.perform_create(result_data)
        response_data = schema.dump(result_data).data
        return {'status': 'success', 'data': response_data, 'message': ''}, 201


class FetchApiView(Resource):
    """
    fetch api view
    """
    def get(self, uuid=None):
        meth = getattr(self.Meta, 'allowed_methods', None)
        schema = getattr(self.Meta, 'schema', None)
        schemas = getattr(self.Meta, 'schemas', None)
        service = self.Meta.service

        sortable = getattr(self.Meta, 'sortable', [])
        filterable = getattr(self.Meta, 'filterable', [])
        params = {"sortable": sortable, "filterable": filterable}
        service(**params)

        request_params = request.args
        if meth and not meth.__contains__(request.method):
            abort(405)

        if uuid:
            data = service.fetch(uuid)
            if not data:
                return {'status': 'error', 'data': {}, 'message': 'No data found'}, 400
            response_data = schema.dump(data)
            return {'status': 'success', 'data': response_data.data, 'message': ''}, 200

        data = service.fetch(None, request_params)

        if not data:
            return {'status': 'error', 'data': {}, 'message': 'No data found'}, 400
        response_data = schemas.dump(data)
        return {'status': 'success', 'data': response_data.data, 'message': ''}, 200


class UpdateApiView(Resource):
    """
    Update api view
    """

    @token_required
    def put(self, uuid=None):
        """
        update api
        :param uuid:
        :return:
        """
        meth = getattr(self.Meta, 'allowed_methods', None)
        schema = getattr(self.Meta, 'schema', None)
        service = self.Meta.service

        if meth and (not meth.__contains__(request.method)):
            abort(405)

        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']

        obj = service.get_details(uuid)
        if not obj:
            return {'status': 'error', 'data': {}, 'message': 'No data found'}, 400
        result_data, errors = schema.load(data, instance=obj, partial=True)
        if errors:
            return {'status': 'error', 'data': {}, 'message': errors}, 422
        result_data = service.perform_update(result_data)
        response_data = schema.dump(result_data).data
        return {'status': 'success', 'data': response_data, 'message': ''}, 200


class ApiView(CreateApiView,
              FetchApiView,
              UpdateApiView):
    """
    api view
    """
    pass
