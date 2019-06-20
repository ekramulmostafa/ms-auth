"""API for Role resource"""
from flask import jsonify, request
from flask_restplus import Namespace, Resource

from app.api.base import DefaultResource, ProtectedResource, ApiView
from app.logging import Logger
from app.models.role import RoleSchema
from app.utils.get_current_user import get_current_user
from app.service.role_service import RoleService


api = Namespace('role')
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

logger = Logger(__name__)


# @api.route('')
# class RoleList(Resource):
#     """Role list functionalities"""
#
#     @api.doc(
#         params={
#             'q': 'query string for searching by name or status',
#             'order_by_field': 'exp: created_at/updated_at/id/name',
#             'order_by': 'exp: desc/none',
#             'limit': 'counter of how many items to fetch',
#             'offset': 'counter from whome position it will start',
#             'datefrom': ' >= date(exp: 2019-03-12)',
#             'dateto': '<= date(exp: 2019-03-12)'
#         })
#     def get(self):
#         """Get all role"""
#
#         logger.info("Get all role")
#
#         filter_object = {
#             'query_string': request.args.get('q', None),
#             # 'order_by_field': request.args.get('order_by_field', None),
#             # 'order_by': request.args.get('order_by', None),
#             # 'datefrom': request.args.get('datefrom', None),
#             # 'dateto': request.args.get('dateto', None),
#             'limit': request.args.get('limit', 0),
#             'offset': request.args.get('offset', 0),
#             'created_at': request.args.get('created_at', None),
#             'active': request.args.get('active', None)
#         }
#
#         param = {
#             'sortable': ['id', '!created_at', 'updated_at'],
#             'filterable': ['active', 'created_at', 'updated_at']
#         }
#
#         role_service = RoleService(**param)
#
#         results = role_service.fetch(None, filter_object)
#
#         return jsonify(results.data)
#
#     @api.doc(
#         params={
#             'name': 'name of the role',
#             'active': 'boolean number and it is nullable',
#             'created_by': 'user uuid',
#             'updated_by': 'user uuid'
#         })
#     def post(self):
#         """Insert a role"""
#         # param = {
#         #     'sortable': ['id', '!created_at', 'updated_at'],
#         #     'filterable': ['active', 'created_at', 'updated_at']
#         # }
#
#         # role_service = RoleService(**param)
#
#         json_data = request.get_json(force=True)
#         if not json_data:
#             return {'message': 'No input data provided'}, 400
#         logger.info("Insert a role", data=json_data)
#         json_data['created_by'] = get_current_user()
#         json_data['updated_by'] = get_current_user()
#
#         param = {
#             'sortable': ['id', '!created_at', 'updated_at'],
#             'filterable': ['active', 'created_at', 'updated_at']
#         }
#
#         role_service = RoleService(**param)
#
#         result = role_service.create(json_data)
#         return {'status': 'success', 'data': result}, 201
#
#
# @api.route('/<uuid:uuid>')
# @api.response(404, 'Role not found')
# class RoleDetail(Resource):
#     """Role detail funtions written"""
#
#     def get(self, uuid):
#         """Get a specific role by id"""
#         logger.info("Get a specific role by Id", data=uuid)
#
#         param = {
#             'sortable': ['id', '!created_at', 'updated_at'],
#             'filterable': ['active', 'created_at', 'updated_at']
#         }
#
#         role_service = RoleService(**param)
#         # role = Role.query.get(uuid)
#         results = role_service.fetch(uuid)
#         return role_schema.jsonify(results)
#
#     @api.doc(
#         params={
#             'name': 'name of the role',
#             'active': 'boolean number and it is nullable',
#             'updated_by': 'user uuid'
#         })
#     def put(self, uuid):
#         """ Update role """
#         # param = {
#         #     'sortable': ['id', '!created_at', 'updated_at'],
#         #     'filterable': ['active', 'created_at', 'updated_at']
#         # }
#
#         # role_service = RoleService(**param)
#
#         logger.info("Update role")
#
#         json_data = request.get_json(force=True)
#         if not json_data:
#             return {'message': 'No input data provided'}, 400
#
#         json_data['updated_by'] = get_current_user()
#
#         param = {
#             'sortable': ['id', '!created_at', 'updated_at'],
#             'filterable': ['active', 'created_at', 'updated_at']
#         }
#
#         role_service = RoleService(**param)
#         result = role_service.update(uuid, json_data)
#
#         return {'status': 'success', 'data': result}, 201


@api.route('/')
class RoleList(ApiView):
    """Test Base functionality"""

    class Meta:
        """meta class"""

        param = {
            'sortable': ['id', '!created_at', 'updated_at'],
            'filterable': ['active', 'created_at', 'updated_at']
        }
        service = RoleService(**param)
        allowed_methods = ['GET', 'POST']
        schema = RoleSchema()
        schemas = RoleSchema(many=True)


@api.route('/<uuid:uuid>/')
class RoleDetail(ProtectedResource):
    """Test Base details functionality"""
    class Meta:
        """meta class"""
        service = RoleService()
