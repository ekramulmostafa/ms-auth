"""Sample Model and Its Manager."""
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

from . import db, ma


class Sample(db.Model):
    """Sample Model."""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """Sample constructor."""
        self.name = kwargs.get('name')

    def save(self, commit=True):
        """Sample save method."""
        db.session.add(self)
        if commit is True:
            db.session.commit()


class SampleSchema(ma.ModelSchema):
    """Sample schema."""
    class Meta:
        """Meta class."""
        model = Sample
