"""User API"""

from flask import request
from flask_restplus import Namespace, Resource

from app.models.users import Users
from app.service.users import UsersServices

user_api = Namespace('user')
user_service = UsersServices()


@user_api.route('/')
class UserListAPI(Resource):
    """User list api"""
    def get(self):
        """GET all users"""

        params = {
            'search': request.args.get('search'),
            'sort_by': request.args.get('sort_by', default='created_at'),
            'order_by': request.args.get('order_by', default='asc'),
            'offset': request.args.get('offset', 0, type=int),
            'limit': request.args.get('limit', 20, type=int),
        }
        users_attrs = list(Users.__dict__.keys())
        for param in request.args:
            if param in users_attrs:
                params[param] = request.args.get(param)

        return user_service.get_all_users(params)

    def post(self):
        """create/signup users"""
        json_data = request.get_json(force=True)
        return user_service.create(json_data['data'])


@user_api.route('/<uuid:uuid>/')
@user_api.param('uuid', 'user identifier')
@user_api.response(404, 'User not found')
class UserDetailAPI(Resource):
    """User details functionality"""
    def get(self, uuid):
        """GET for User API Details"""
        return user_service.get_user_details(uuid)

    def put(self, uuid):
        """PUT for User API Update"""
        data = request.json
        return user_service.update(data['data'], uuid)


@user_api.route('/login/')
class UserLoginAPI(Resource):
    """User details functionality"""

    def post(self):
        """login user"""
        json_data = request.get_json(force=True)
        return user_service.login(json_data['data'])
