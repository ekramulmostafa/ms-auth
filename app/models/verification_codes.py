"""User model"""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ChoiceType

from app.models.model_mixin import TimestampMixin
from . import db


class VerificationCodes(TimestampMixin, db.Model):
    """verification codes model"""

    TYPES = [
        (1, 'Password-reset'),
        (2, 'Verification'),
    ]
    STATUS = [
        (1, 'New'),
        (2, 'Used'),
    ]
    EXPIRY_DAYS = 7

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    verified_user = db.relationship('Users', foreign_keys=[user_id], backref='verifications')

    code = db.Column(db.String(100), nullable=False, unique=True)
    expired_at = db.Column(db.DateTime,
                           nullable=True,
                           default=datetime.utcnow()+timedelta(days=EXPIRY_DAYS))
    types = db.Column(db.Integer, ChoiceType(TYPES), nullable=False)
    status = db.Column(db.Integer, ChoiceType(STATUS), nullable=False)

    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    updated_by_user_verification = db.relationship("Users", foreign_keys=[updated_by])
    created_by_user_verification = db.relationship("Users", foreign_keys=[created_by])

    def save(self, commit=True):
        """VerificationCodes save method"""
        db.session.add(self)
        if commit is True:
            db.session.commit()

    @staticmethod
    def save_verification_code(**kwargs):
        """save verification code to db"""
        try:
            code = kwargs['code']
        except KeyError:
            code = uuid.uuid4()

        obj = VerificationCodes(verified_user=kwargs['user'],
                                code=code,
                                types=kwargs['types'],
                                status=kwargs['status'],
                                created_by=str(kwargs['user'].id))
        db.session.add(obj)
        db.session.commit()
        return obj
