"""Model for Role resource"""
from app.models.role_permission import RolePermission
import datetime
from datetime import datetime as dateconverterdatetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, or_, and_
from app.models.permission import Permission, PermissionSchema
from . import db, ma

from marshmallow import fields


class Role(db.Model):
    """Description for role model"""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    permissions = db.relationship('Permission', secondary='role_permission',
                                  backref=db.backref('roles'))

    def __init__(self, **kwargs):
        """Initialization for role model"""
        self.name = kwargs.get('name')
        self.active = kwargs.get('active', True)
        self.created_by = kwargs.get('created_by')
        self.updated_by = kwargs.get('updated_by')

    def save(self, commit=True):
        """Save data for role model"""
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def save_role_permission(self, permission, commit=True):
        self.permissions.append(permission)
        db.session.add(self)
        if commit is True:
            db.session.commit()

    @classmethod
    def get_roles(cls, filter_object):
        """Get roles"""
        all_roles = Role.query
        if filter_object['query_string']:
            if filter_object['query_string'] == 'true' or filter_object['query_string'] == 'false':
                all_roles = all_roles.filter(Role.active == filter_object['query_string'])
            else:
                all_roles = all_roles.filter(
                    Role.name.like("%" + filter_object['query_string'] + "%"))

        if filter_object['datefrom'] and filter_object['dateto']:
            date_from_obj = dateconverterdatetime.strptime(filter_object['datefrom'], '%Y-%m-%d')
            date_to_obj = dateconverterdatetime.strptime(filter_object['dateto'], '%Y-%m-%d')
            all_roles = all_roles.filter(
                or_(
                    and_(Role.created_at >= date_from_obj,
                         Role.created_at <= date_to_obj),
                    and_(Role.updated_at >= date_from_obj,
                         Role.updated_at <= date_to_obj)))

        all_roles = Role.get_order_by_filter(all_roles, filter_object)

        if int(filter_object['limit']) > 0:
            all_roles = all_roles.limit(filter_object['limit'])

        if int(filter_object['offset']) > 0:
            all_roles = all_roles.offset(filter_object['offset'])

        all_roles = all_roles.all()

        return all_roles

    @classmethod
    def get_order_by_filter(cls, all_roles, filter_object):
        """Private method: Get Order by filter"""
        if filter_object['order_by_field'] == "created_at":
            if filter_object['order_by'] == "desc":
                all_roles = all_roles.order_by(desc(Role.created_at))
            else:
                all_roles = all_roles.order_by(Role.created_at)
        elif filter_object['order_by_field'] == "updated_at":
            if filter_object['order_by'] == "desc":
                all_roles = all_roles.order_by(desc(Role.updated_at))
            else:
                all_roles = all_roles.order_by(Role.updated_at)
        elif filter_object['order_by_field'] == "id":
            if filter_object['order_by'] == "desc":
                all_roles = all_roles.order_by(desc(Role.id))
            else:
                all_roles = all_roles.order_by(Role.id)
        return all_roles


# class RolePermission(db.Model):
#     """Description for role permission model"""
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), primary_key=True)
#     permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('permission.id'), primary_key=True)

#     @classmethod
#     def save(cls, role, permission):
#         role.role_permission.append(permission)
#         db.session.add(role)
#         db.session.commit()


class RoleSchema(ma.ModelSchema):
    """Role model Schema"""
    permissions = fields.Nested(PermissionSchema, many=True)

    class Meta:
        """Role model meta"""
        model = Role
