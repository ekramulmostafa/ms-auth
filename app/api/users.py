"""User API"""

from flask import request, session
from flask_restplus import Namespace, Resource

from app.api.base import DefaultResource, ProtectedResource
from app.models.users import Users
from app.service.users import UsersServices, UserTestService
from app.utils.decorator import token_required

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


@user_api.route('/forget-password/')
class UserForgetPasswordAPI(Resource):
    """User forget password functionality"""

    def post(self):
        """POST for User forget password"""
        data = request.json
        return user_service.forget_password(data['data'])


@user_api.route('/verify/<string:code>/')
class UserVerificationAPI(Resource):
    """User verification functionality"""
    def get(self, code):
        """GET for User verification"""
        return user_service.verify_user(code)


@user_api.route('/password-reset/<string:code>/')
class UserResetPasswordAPI(Resource):
    """User reset password functionality"""

    def post(self, code):
        """POST for User reset password"""
        data = request.json
        return user_service.reset_password(data['data'], code)


@user_api.route('/current-user/')
class CurrentUserAPI(Resource):
    """Current User functionality"""
    @token_required
    def get(self):
        """GET for current user"""
        user = session['current_user']
        return user_service.get_user_details(uuid=user['id'])

    @token_required
    def put(self):
        """PUT for Current User API Update"""
        data = request.json
        user = session['current_user']
        data['data']['updated_by'] = user['id']
        return user_service.update(data['data'], uuid=user['id'])


@user_api.route('/current-user/update-password/')
class CurrentUserUpdatePasswordAPI(Resource):
    """Current User only password update functionality"""
    @token_required
    def put(self):
        """PUT for Current User API Update"""
        data = request.json
        user = Users.query.get(session['current_user']['id'])
        return user_service.update_password(data['data'], user=user)


@user_api.route('/log/')
class TestBaseAPI(DefaultResource):
    """Test Base functionality"""
    class Meta:
        """meta class"""
        service = UsersServices()
        methods = ['GET', 'POST']


@user_api.route('/log/<uuid:uuid>/')
class TestBaseDetailsAPI(ProtectedResource):
    """Test Base details functionality"""
    class Meta:
        """meta class"""
        service = UserTestService()
