"""Permission Model and Its Manager."""
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, asc


from . import db, ma

class PermissionModel(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    active = db.Column(db.Boolean,nullable=False)
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
            result = db.session.commit()
            return result     

    def get_permission(args,**kwargs):
        
        search = kwargs.get('search', None)
        filterBy  = kwargs.get('filter_by')
        sortBy =  kwargs.get('sort_by','asc')
        limit = kwargs.get('limit',10)
        offset = kwargs.get('offset',0)

        allPermission =  PermissionModel.query
        if search:
            result = allPermission.filter(PermissionModel.name.like('%'+search+'%')).offset(offset).limit(limit).all()
        if filterBy =='active':
            result = allPermission.query.filter_by(active=True).offset(offset).limit(limit).all()
        elif filterBy:
            if sortBy == 'desc':
                result = allPermission.order_by(desc(getattr(PermissionModel, filterBy))).offset(offset).limit(limit).all()
            else:
                result = allPermission.order_by(asc(getattr(PermissionModel, filterBy))).offset(offset).limit(limit).all()
        else:
            result = allPermission.offset(offset).limit(limit).all()
        return result 


class PermissionSchema(ma.ModelSchema):
    """Permission Schema """
    class Meta: 
        """ Meta class """
        model = PermissionModel
        fields = ("id", "name", "code", "active",'created_at','updated_at')
        ordered = True