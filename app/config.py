"""Test configuration."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:12345678@localhost:5433/ms-template'
    )


class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """Test config."""
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StagingConfig(Config):
    """Stage config."""
    DEBUG = True


class ProductionConfig(Config):
    """Production config."""
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    stage=StagingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
