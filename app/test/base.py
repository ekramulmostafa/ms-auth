from flask_testing import TestCase
from app.models import db
from manage import app


class BaseTestCase(TestCase):
    """
    Base tests
    """
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
