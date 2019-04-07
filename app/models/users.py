"""User model"""

import uuid
from datetime import datetime
from sqlalchemy_utils import ChoiceType

from sqlalchemy.dialects.postgresql import UUID

from app.models.model_mixin import TimestampMixin

from app.models.role import Role

from app.models.user_role import UserRole

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
    verifications = db.relationship('VerificationCodes', backref='verified_user')

    status = db.Column(db.Integer, ChoiceType(STATUS), nullable=False, default=1)
    active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    roles = db.relationship(Role, secondary=UserRole.__tablename__, backref=db.backref('users'))

    def save(self, commit=True):
        """save method"""
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def save_user_role(self, role, commit=True):
        """save method"""
        self.roles.append(role)
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def edit_user_role(self, role, commit=True):
        """ edit user """
        self.roles.append(role)
        db.session.add(self)
        if commit is True:
            db.session.commit()
