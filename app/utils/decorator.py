"""decorator"""
from functools import wraps
from flask import request, session

from app.models.users import Users
from app.utils.utils import decode_auth_token


def token_required(f):
    """ bearer token required"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            prefix, token = auth_token.split(' ')
            if prefix != 'Bearer':
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': 'Invalid Bearer token'
                }
                return response_object, 401

            resp = decode_auth_token(token)
            if resp['status'] == 'error':
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': resp['message']
                }
                return response_object, 401
            user = Users.query.filter_by(id=resp['data']['sub']).first()
            if user:
                session['current_user'] = user
            else:
                response_object = {
                    'status': 'error',
                    'data': {},
                    'message': 'no user found with this token'
                }
                return response_object, 401

        return f(*args, **kwargs)

    return wrapped
