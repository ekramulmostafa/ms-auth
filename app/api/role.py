"""API for Role resource"""
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role import Role, RoleSchema
from app.utils.get_current_user import get_current_user

api = Namespace('role')
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

logger = Logger(__name__)


@api.route('')
class RoleList(Resource):
    """Role list functionalities"""
    @api.doc(
        params={
            'q': 'query string for searching by name or status',
            'order_by_field': 'exp: created_at/updated_at/id/name',
            'order_by': 'exp: desc/none',
            'limit': 'counter of how many items to fetch',
            'offset': 'counter from whome position it will start',
            'datefrom': ' >= date(exp: 2019-03-12)',
            'dateto': '<= date(exp: 2019-03-12)'
        })
    def get(self):
        """Get all role"""

        logger.info("Get all role")

        filter_object = {
            'query_string': request.args.get('q', None),
            'order_by_field': request.args.get('order_by_field', None),
            'order_by': request.args.get('order_by', None),
            'datefrom': request.args.get('datefrom', None),
            'dateto': request.args.get('dateto', None),
            'limit': request.args.get('limit', 0),
            'offset': request.args.get('offset', 0)
        }

        roles = Role.get_roles(filter_object)

        result = roles_schema.dump(roles)
        return jsonify(result.data)

    @api.doc(
        params={
            'name': 'name of the role',
            'active': 'boolean number and it is nullable',
            'created_by': 'user uuid',
            'updated_by': 'user uuid'
        })
    def post(self):
        """Insert a role"""

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        logger.info("Insert a role", data=json_data)
        json_data['created_by'] = get_current_user()
        json_data['updated_by'] = get_current_user()
        # Validate and deserialize input
        role, errors = role_schema.load(json_data)
        if errors:
            logger.warning("Insert role error", data=errors)
            return errors, 422
        role.save()
        result = role_schema.dump(role).data
        return {'status': 'success', 'data': result}, 201


@api.route('/<uuid:uuid>')
@api.response(404, 'Role not found')
class RoleDetail(Resource):
    """Role detail funtions written"""

    def get(self, uuid):
        """Get a specific role by id"""
        logger.info("Get a specific role by Id", data=uuid)

        role = Role.query.get(uuid)
        return role_schema.jsonify(role)

    @api.doc(
        params={
            'name': 'name of the role',
            'active': 'boolean number and it is nullable',
            'updated_by': 'user uuid'
        })
    def put(self, uuid):
        """ Update role """
        logger.info("Update role")

        role_obj = Role.query.get(uuid)
        if role_obj is None:
            return {'message': 'Role not found'}, 404

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        json_data['updated_by'] = get_current_user()

        role, errors = role_schema.load(json_data, instance=role_obj, partial=True)
        if errors:
            logger.warning("Update role error", data=errors)
            return errors, 422

        role.save()
        result = role_schema.dump(role).data
        return {'status': 'success', 'data': result}, 201
