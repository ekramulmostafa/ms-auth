"""Model for Role resource"""
import datetime
from datetime import datetime as dateconverterdatetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, or_, and_
from marshmallow import fields
from app.models.permission import PermissionSchema
from app.models.role_permission import RolePermission
from . import db, ma


class Role(db.Model):
    """Description for role model"""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now, nullable=False)

    permissions = db.relationship('Permission', secondary=RolePermission.__tablename__,
                                  backref=db.backref('roles'))

    def __init__(self, **kwargs):
        """Initialization for role model"""
        self.name = kwargs.get('name')
        self.active = kwargs.get('active', True)
        self.created_by = kwargs.get('created_by')
        self.updated_by = kwargs.get('updated_by')

    def save(self, commit=True):
        """Save data for role model"""

        db.session.add(self)
        if commit is True:
            db.session.commit()

    def save_role_permission(self, permission, commit=True):
        """Relationship between role and permission"""
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
        if filter_object['order_by_field'] in Role.__dict__:
            if filter_object['order_by'] == "desc":
                all_roles = all_roles.order_by(desc(Role.__dict__[filter_object['order_by_field']]))
            else:
                all_roles = all_roles.order_by(Role.__dict__[filter_object['order_by_field']])

        return all_roles


class RoleSchema(ma.ModelSchema):
    """Role model Schema"""
    id = fields.String()
    name = fields.String()
    active = fields.Boolean()
    created_by = fields.String()
    updated_by = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    permissions = fields.Nested(PermissionSchema, many=True)

    class Meta:
        """Role model meta"""
        model = Role
        fields = ('id', 'active', 'name', 'created_by', 'updated_by', 'created_at', 'updated_at')
