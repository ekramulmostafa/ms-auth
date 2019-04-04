""" User role Model design """
import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
# from app.models.role import Role
from app.models import ma
from . import db


class UserRole(db.Model):
    """ User role model """
    __tablename__ = 'user_role'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = db.Column(UUID, db.ForeignKey('role.id'), nullable=False)
    user_id = db.Column(UUID, db.ForeignKey('users.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=1)
    update_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, **arg):
        """ User role cobstructor """
        self.role_id = arg.get('role_id')
        self.user_id = arg.get('user_id')
        self.active = arg.get('active')

    def save(self, commit=True):
        """ User role save """
        if commit:
            db.session.add(self)
            db.session.commit()

    def get_by_uid_rid(self, user_id, role_id):
        """ User role uid rid """
        search = {
            "user_id": user_id,
            "role_id": role_id
        }
        user_role = UserRole.query
        result = user_role.filter_by(**search).first()
        return result


class UserRoleSchema(ma.ModelSchema):
    """ User role schema """
    class Meta:
        """ User role Meta """
        model = UserRole
        fields = ('id', 'role_id', 'user_id', 'active')
