"""common model mixins"""

from datetime import datetime
from . import db


class TimestampMixin:
    """timestame model mixin"""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
