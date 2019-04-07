"""User model"""

import uuid

from sqlalchemy_utils import ChoiceType
from sqlalchemy.dialects.postgresql import UUID

from app.models.model_mixin import TimestampMixin

from . import db


class Users(TimestampMixin, db.Model):
    """User model"""

    STATUS = [
        (1, 'Regular'),
        (2, 'Locked'),
        (3, 'Blocked')
    ]
    __searchable__ = ['first_name', 'last_name', 'email']

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(130), nullable=False)

    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.Integer, ChoiceType(STATUS), nullable=False, default=1)
    active = db.Column(db.Boolean, nullable=False, default=True)

    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))

    def save(self, commit=True):
        """save method"""
        db.session.add(self)
        if commit is True:
            db.session.commit()
