"""Model for Base Model resource"""
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from . import db


class BaseModel(db.Model):
    """Description for base model"""
    __abstract__ = True
    __searchable__ = []
    __filterable__ = {}

    @declared_attr
    def created_by(self):
        """common foreign key attribute"""
        return db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    @declared_attr
    def updated_by(self):
        """common foreign key attribute"""
        return db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now, nullable=False)
