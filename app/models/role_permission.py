"""Model for Role Permission resource"""
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import and_

from . import db, ma


class RolePermission(db.Model):
    """Description for role permission model"""
    __table_args__ = (
        db.UniqueConstraint('role_id', 'permission_id', name='unique_role_permission'),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('permission.id'))

    status = db.Column(db.Boolean(), nullable=False, default=True)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    @classmethod
    def get_by_role_permission(cls, role_id, permisson_id):
        """GET data for role permission model"""
        role_permission_obj = RolePermission.query.filter(
            and_(RolePermission.role_id == role_id,
                 RolePermission.permission_id == permisson_id)
        ).first()
        return role_permission_obj

    def save_data(self, commit=True):
        """Save data for role permission model"""
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def delete(self, commit=True):
        """Delete data for role permission model"""
        db.session.delete(self)
        if commit is True:
            db.session.commit()


class RolePermissionSchema(ma.ModelSchema):
    """Role Permission model Schema"""

    class Meta:
        """Role Permission model meta"""
        model = RolePermission
        fields = ('id', 'role_id', 'permission_id', 'status', 'created_by', 'updated_by')
