"""User API"""

from flask import request, session
from flask_restplus import Namespace, Resource

from app.api.base import ApiResource
from app.models.users import Users
from app.serializers.users import UsersModelSchema
from app.service.users import UserServices
from app.utils.decorator import token_required

user_api = Namespace('user')
user_service = UserServices()


@user_api.route('/')
class UserListAPI(ApiResource):
    """Test Base functionality"""
    class Meta:
        """meta class"""

        filterable = ['first_name', 'username', 'email']
        service = UserServices()
        allowed_methods = ['GET', 'POST']
        schema = UsersModelSchema()
        schemas = UsersModelSchema(many=True)


@user_api.route('/<uuid:uuid>/')
class UserDetailsAPI(ApiResource):
    """Test Base details functionality"""
    class Meta:
        """meta class"""

        service = UserServices()
        allowed_methods = ['GET', 'PUT']
        schema = UsersModelSchema()
        schemas = UsersModelSchema(many=True)


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
