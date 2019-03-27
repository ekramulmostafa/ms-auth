"""Test configuration."""
from flask import current_app
from flask_testing import TestCase

from manage import app


class TestDevelopmentConfig(TestCase):
    """Test deve releted test cases."""
    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """test config related to development profile."""
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    """Test test releted test cases."""
    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """test config related to test profile."""
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])


class TestStatgingConfig(TestCase):
    """Test stage releted test cases."""
    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.StagingConfig')
        return app

    def test_app_is_testing(self):
        """test config related to stage profile."""
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


class TestProductionConfig(TestCase):
    """Test prod releted test cases."""
    def create_app(self):
        """Create app."""
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """test config related to prod profile."""
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
