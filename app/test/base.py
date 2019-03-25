""" Base Test Class"""
from flask_testing import TestCase
from manage import app
from app.models import db


class BaseTestCase(TestCase):
    """
    Base tests
    """
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
