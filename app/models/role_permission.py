"""Model for Role resource"""
import datetime
from datetime import datetime as dateconverterdatetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, or_, and_

from app.models.role import Role
from app.models.permission import Permission
from . import db, ma


class RolePermission(db.Model):
    """Description for role permission model"""
    __tablename__ = 'role_permission'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

    role = db.relationship("Role", back_populates="permissions")
    permissions = db.relationship("Permission", back_populates="roles")
