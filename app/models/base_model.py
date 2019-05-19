"""Model for Base Model resource"""
import datetime

from . import db, ma


class BaseModel(db.Model):
    """Description for base model"""
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now, nullable=False)

    def save(self, commit=True):
        """Generic Save data"""

        db.session.add(self)
        if commit is True:
            db.session.commit()
