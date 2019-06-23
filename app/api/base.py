""" API base class """

from flask_restplus import Resource, abort
from flask import request, session

from app.utils.decorator import token_required


class CreateApiResource(Resource):
    """
    create api view
    """
    def post(self, *args, **kwargs):
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


class FetchApiResource(Resource):
    """
    fetch api view
    """
    def get(self, uuid=None, *args, **kwargs):
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


class UpdateApiResource(Resource):
    """
    Update api view
    """
    def put(self, uuid=None, *args, **kwargs):
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


class AuthorizedCreateApiResource(CreateApiResource):
    """
    protected create api view
    """

    @token_required
    def post(self, *args, **kwargs):
        """
        post api
        :param uuid:
        :return:
        """
        kwargs['token'] = True
        return super().post(*args, **kwargs)


class AuthorizedFetchApiResource(FetchApiResource):
    """
    protected Update api view
    """

    @token_required
    def get(self, uuid=None, *args, **kwargs):
        """
        get api
        :param uuid:
        :return:
        """
        kwargs['token'] = True
        return super().get(uuid, *args, **kwargs)


class AuthorizedUpdateApiResource(UpdateApiResource):
    """
    protected Update api view
    """

    @token_required
    def put(self, uuid=None, *args, **kwargs):
        """
        update api
        :param uuid:
        :return:
        """
        kwargs['token'] = True
        return super().put(uuid, *args, **kwargs)


class ApiResource(CreateApiResource,
                  FetchApiResource,
                  UpdateApiResource):
    """
    api view
    """
    pass


class AuthorizedApiResource(AuthorizedCreateApiResource,
                            AuthorizedFetchApiResource,
                            AuthorizedUpdateApiResource):
    """
    Authorized api view
    """
    pass
