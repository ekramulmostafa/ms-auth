"""Models for the service."""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma: Marshmallow = Marshmallow()
__all__ = ['sample', 'role']
