"""This creates api."""
from flask import Blueprint
from flask_restplus import Api

from .sample import api as sample
from .permission import api as permission


blueprint_api = Blueprint('api', __name__, url_prefix='/v1')
api = Api(
    blueprint_api,
    title='MS-Template API',
    version='1.0',
    description='This is a test service',
    doc='/doc/'
)

api.add_namespace(sample)
api.add_namespace(permission)
