""" API base class """

from flask_restplus import Resource, abort
from flask import request, session

from app.utils.decorator import token_required


class BaseApi(Resource):
    """
    resource base api
    """
    class Meta:
        """meta class"""
        service = None
        allowed_methods = None
        schema = None
        schemas = None

    def post(self, **kwargs):
        """
        :param kwargs:
        :return:
        """

    def get(self, uuid=None, **kwargs):
        """
        :param uuid:
        :param args:
        :param kwargs:
        :return:
        """

    def put(self, uuid=None, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """


class ApiResource(BaseApi):
    """
    resource api
    """
    def post(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
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

    def get(self, uuid=None, **kwargs):
        """
        :param uuid:
        :return:
        """
        meth = getattr(self.Meta, 'allowed_methods', None)
        schema = getattr(self.Meta, 'schema', None)
        schemas = getattr(self.Meta, 'schemas', None)
        service = self.Meta.service

        sortable = getattr(self.Meta, 'sortable', [])
        filterable = getattr(self.Meta, 'filterable', [])
        params = {"sortable": sortable, "filterable": filterable}

        service.__call__(**params)

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

    def put(self, uuid=None, **kwargs):
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

        is_token_required = kwargs.pop('token', False)
        if is_token_required:
            user = session['current_user']
            data['data']['updated_by'] = user['id']

        obj = service.fetch(uuid)
        if not obj:
            return {'status': 'error', 'data': {}, 'message': 'No data found'}, 400
        result_data, errors = schema.load(data['data'], instance=obj, partial=True)
        if errors:
            return {'status': 'error', 'data': {}, 'message': errors}, 422
        result_data = service.perform_update(result_data)
        response_data = schema.dump(result_data).data
        return {'status': 'success', 'data': response_data, 'message': ''}, 200


class AuthorizedApiResource(ApiResource):
    """
    protected create api view
    """

    @token_required
    def post(self, **kwargs):
        """
        post api
        :return:
        """
        kwargs['token'] = True
        return super().post(**kwargs)

    @token_required
    def get(self, uuid=None, **kwargs):
        """
        get api
        :param uuid:
        :return:
        """
        kwargs['token'] = True
        return super().get(uuid, **kwargs)

    @token_required
    def put(self, uuid=None, **kwargs):
        """
        update api
        :param uuid:
        :return:
        """
        kwargs['token'] = True
        return super().put(uuid, **kwargs)
