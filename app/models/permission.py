"""Permission Model and Its Manager."""
import datetime
import uuid
from sqlalchemy import desc, asc, or_
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
from . import db, ma


class PermissionModel(db.Model):
    """ permission table model """
    __tablename__ = 'permissions'

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
        sortBy = kwargs.get('sort_by', 'active')
        orderBy = kwargs.get('order_by', 'asc')
        limit = kwargs.get('limit', 10)
        offset = kwargs.get('offset', 0)
        filterBy = {}
        # check whether there is filtering option for that
        mapper = inspect(PermissionModel)
        for column in mapper.attrs:
            if kwargs.get(column.key):
                filterBy[column.key] = kwargs.get(column.key)

        allPermission = PermissionModel.query
        if search:
            result = allPermission.filter(
                or_(PermissionModel.name.like('%'+search+'%'), PermissionModel.code.like(
                    '%'+search+'%'))).order_by(desc(getattr(PermissionModel, sortBy))
                                               ).offset(offset).limit(limit).all()
        elif filterBy:
            result = allPermission.filter_by(**filterBy).offset(offset).limit(limit).all()
        # this will sort by field name either asc or desc
        elif sortBy:
            if orderBy == 'desc':
                result = allPermission.order_by(desc(getattr(PermissionModel, sortBy))
                                                ).offset(offset).limit(limit).all()
            else:
                result = allPermission.order_by(asc(getattr(PermissionModel, sortBy))
                                                ).offset(offset).limit(limit).all()
        else:
            result = allPermission.offset(offset).limit(limit).all()
        return result


class PermissionSchema(ma.ModelSchema):
    """Permission Schema """
    class Meta:
        """ Meta class """
        model = PermissionModel
        fields = ("id", "name", "code", "active", 'created_at', 'updated_at')
        ordered = True
