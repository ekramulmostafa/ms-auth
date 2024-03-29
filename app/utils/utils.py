"""utils"""

import jwt
from flask_mail import Message
from flask import current_app as app

from app.service import mail


def send_email(data: dict):
    """send email"""
    msg = Message(**data)
    mail.send(msg)
    return True


def encode_auth_token(payload=None):
    """ generate jwt token"""
    token = jwt.encode(
        payload,
        app.config.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    )
    return token.decode()


def decode_auth_token(auth_token):
    """Decodes the auth token"""
    try:
        payload = jwt.decode(auth_token, app.config.get('JWT_SECRET_KEY'))
        return {'status': 'success', 'data': payload, 'message': ''}
    except jwt.ExpiredSignatureError:
        return {'status': 'error', 'data': {}, 'message': 'token expired'}
    except jwt.InvalidTokenError:
        return {'status': 'error', 'data': {}, 'message': 'invalid token'}
