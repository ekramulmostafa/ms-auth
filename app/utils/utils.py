"""utils"""

from uuid import uuid4

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


def save_verification_code(**kwargs):
    """save verification code to db"""
    verification_code_schema = VerificationCodesModelSchema()
    try:
        code = kwargs['code']
    except KeyError:
        code = uuid4()

    obj = VerificationCodes(verified_user=kwargs['user'],
                            code=code,
                            types=kwargs['types'],
                            status=kwargs['status'],
                            created_by=str(kwargs['user'].id))
    db.session.add(obj)
    db.session.commit()
    response_data = verification_code_schema.dump(obj).data

    return response_data
