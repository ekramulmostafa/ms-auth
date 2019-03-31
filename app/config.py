"""Test configuration."""
import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:12345678@localhost:5432/ms-auth'
    )
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    """Test config."""
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:12345678@localhost:5432/ms-auth'
    )
    SQLALCHEMY_DATABASE_URI = '{}-test'.format(SQLALCHEMY_DATABASE_URI)


class StagingConfig(Config):
    """Stage config."""
    DEBUG = True
    LOG_LEVEL = logging.WARNING


class ProductionConfig(Config):
    """Production config."""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    stage=StagingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
