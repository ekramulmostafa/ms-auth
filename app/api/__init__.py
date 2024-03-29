"""This creates api."""

from flask import Blueprint
from flask_restplus import Api

from .sample import api as sample
from .permission import api as permission
from .users import user_api as user
from .role import api as role
from .user_role import api as user_role
from .role_permission import api as role_permission

blueprint_api = Blueprint('auth', __name__, url_prefix='/v1')
api = Api(
    blueprint_api,
    title='MS-Auth API',
    version='1.0',
    description='This is auth service',
    doc='/doc/'
)

api.add_namespace(sample)
api.add_namespace(permission)
api.add_namespace(user)
api.add_namespace(role)
api.add_namespace(user_role)
api.add_namespace(role_permission)
