"""Model for Role Permission resource"""
import datetime
from datetime import datetime as dateconverterdatetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, or_, and_

from . import db, ma

from marshmallow import fields


class RolePermission(db.Model):
    """Description for role permission model"""
    __tablename__ = 'role_permission'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('permission.id'), primary_key=True)

    status = db.Column(db.Boolean(), nullable=False, default=True)
    created_by = db.Column(db.String(100), nullable=False, default='10101010101')
    updated_by = db.Column(db.String(100), nullable=False, default='10101010101')
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)


class RolePermissionSchema(ma.ModelSchema):
    """Role Permission model Schema"""

    class Meta:
        """Role Permission model meta"""
        model = RolePermission
