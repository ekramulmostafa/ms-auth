"""User model"""

import uuid

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
        (3, 'Expired')
    ]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    verified_user = db.relationship('Users', foreign_keys=[user_id], backref='verifications')

    code = db.Column(db.String(100), nullable=False)
    expired_at = db.Column(db.DateTime, nullable=True)
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
