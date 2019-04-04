"""utils"""

import random
import string


from flask_mail import Message

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


def save_verification_code(data: dict):
    """generate random 6 character string"""
    verification_code_schema = VerificationCodesModelSchema()
    code = generate_random_string()

    obj = VerificationCodes(verified_user=data['user'],
                            code=code,
                            types=data['types'],
                            status=data['status'])
    db.session.add(obj)
    db.session.commit()
    response_data = verification_code_schema.dump(obj).data

    return response_data
