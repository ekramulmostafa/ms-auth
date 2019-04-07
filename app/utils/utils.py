"""utils"""

import random
import string
import flask_bcrypt

import jwt
from flask_mail import Message
from flask import current_app as app

from app.models import db

from app.models.verification_codes import VerificationCodes
from app.serializers.verification_codes import VerificationCodesModelSchema
from app.service import mail


def send_email(data: dict):
    """send email"""
    msg = Message(**data)
    mail.send(msg)
    return True


DEFAULT_CHAR_STRING = string.ascii_uppercase+string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    """generate random 6 character string"""
    return ''.join(random.choice(chars) for _ in range(size))


def generate_password(password):
    """generate password"""
    password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    return password_hash


def check_password(password_hash, password):
    """check password is correct"""
    is_correct_password = flask_bcrypt.check_password_hash(password_hash,
                                                           password)
    return is_correct_password


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


def save_verification_code(**kwargs):
    """generate random 6 character string"""
    verification_code_schema = VerificationCodesModelSchema()
    try:
        code = kwargs['code']
    except KeyError:
        code = generate_random_string()

    obj = VerificationCodes(verified_user=kwargs['user'],
                            code=code,
                            types=kwargs['types'],
                            status=kwargs['status'])
    db.session.add(obj)
    db.session.commit()
    response_data = verification_code_schema.dump(obj).data

    return response_data
