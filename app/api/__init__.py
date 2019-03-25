"""This creates api."""
from flask import Blueprint
from flask_restplus import Api

from .sample import api as sample


blueprint_api = Blueprint('auth', __name__, url_prefix='/v1')
api = Api(
    blueprint_api,
    title='MS-Auth API',
    version='1.0',
    description='This is auth service',
    doc='/doc/'
)

api.add_namespace(sample)
