"""Test init."""
from flask_testing import TestCase

from manage import app
from app.models import db


class BaseTest(TestCase):
    """Test dev releted test cases."""

    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
