"""User model"""

import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ChoiceType

from app.models.role import Role
from . import db


class Users(db.Model):
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

    verification_code = db.Column(db.String(130), nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.Integer, ChoiceType(STATUS), nullable=False, default=1)
    active = db.Column(db.Boolean, nullable=False, default=True)
    # TODO : 'roles' will be deleted after bon-104 merged
    roles = db.relationship('Role', secondary="user_role", backref='users', cascade="all, delete")

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    def save(self, commit=True):
        """save method"""
        # TODO : will be deleted after bon-104 merged
        self.roles.append(Role.query.first())
        db.session.add(self)
        if commit is True:
            db.session.commit()


class UserRole(db.Model):
    """temporary user role model"""
    # TODO : will be deleted after bon-104 merged
    __tablename__ = "user_role"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id', ondelete='CASCADE'))
