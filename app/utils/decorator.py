"""decorator"""
from functools import wraps
from flask import request, session

from app.models.users import Users
from app.serializers.users import UsersModelSchema
from app.utils.utils import decode_auth_token

user_schema = UsersModelSchema()


def token_required(f):
    """ bearer token required"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            token = auth_token.split(' ')
            if (token[0] != 'Bearer') or (len(token) < 2):
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': 'Invalid Bearer token'
                }
                return response_object, 401

            resp = decode_auth_token(token[1])
            if resp['status'] == 'error':
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': resp['message']
                }
                return response_object, 401
            user = Users.query.filter_by(id=resp['data']['sub']).first()
            if not user:
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': 'no user found with this token'
                }
                return response_object, 401

            session['current_user'] = user_schema.dump(user).data
        else:
            response_object = {
                'status': 'error',
                'data': {},
                'message': 'no authorization token found'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return wrapped
