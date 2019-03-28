"""Permission Model and Its Manager."""
import datetime
import uuid
from sqlalchemy import desc, asc, or_
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
from . import db, ma


class Permission(db.Model):
    """ permission table model """

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """constructor."""
        self.name = kwargs.get('name')
        self.code = kwargs.get('code')
        self.active = kwargs.get('active')

    def save(self, commit=True):
        """Permission save method."""
        db.session.add(self)
        if commit is True:
            db.session.commit()

    def get_permission(self, **kwargs):
        """ this is common method for returing list of permission including filter & search"""
        search = kwargs.get('search', None)
        sort_by = kwargs.get('sort_by', 'active')
        order_by = kwargs.get('order_by', 'asc')
        limit = kwargs.get('limit', 10)
        offset = kwargs.get('offset', 0)
        filter_by = {}
        # check whether there is filtering option for that
        mapper = inspect(Permission)
        for column in mapper.attrs:
            if kwargs.get(column.key):
                filter_by[column.key] = kwargs.get(column.key)

        all_permission = Permission.query
        if search:
            result = all_permission.filter(
                or_(Permission.name.like('%'+search+'%'), Permission.code.like(
                    '%'+search+'%'))).order_by(desc(getattr(Permission, sort_by))
                                               ).offset(offset).limit(limit).all()
        elif filter_by:
            result = all_permission.filter_by(**filter_by).offset(offset).limit(limit).all()
        # this will sort by field name either asc or desc
        elif sort_by:
            if order_by == 'desc':
                result = all_permission.order_by(desc(getattr(Permission, sort_by))
                                                 ).offset(offset).limit(limit).all()
            else:
                result = all_permission.order_by(asc(getattr(Permission, sort_by))
                                                 ).offset(offset).limit(limit).all()
        else:
            result = all_permission.offset(offset).limit(limit).all()
        return result


class PermissionSchema(ma.ModelSchema):
    """Permission Schema """
    class Meta:
        """ Meta class """
        model = Permission
        fields = ("id", "name", "code", "active", 'created_at', 'updated_at')
        ordered = True
