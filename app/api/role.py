"""API for Role resource"""
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.role import Role, RoleSchema

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
            'order_by_field': 'exp: created_at/updated_at/id',
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
            'query_string': None,
            'order_by_field': None,
            'order_by': None,
            'datefrom': None,
            'dateto': None,
            'limit': 0,
            'offset': 0
        }

        if request.args.get('q'):
            filter_object['query_string'] = request.args.get('q')
        if request.args.get('order_by_field'):
            filter_object['order_by_field'] = request.args.get('order_by_field')
        if request.args.get('order_by'):
            filter_object['order_by'] = request.args.get('order_by')

        if request.args.get('limit'):
            filter_object['limit'] = request.args.get('limit')
        if request.args.get('offset'):
            filter_object['offset'] = request.args.get('offset')

        if request.args.get('datefrom'):
            filter_object['datefrom'] = request.args.get('datefrom')
        if request.args.get('dateto'):
            filter_object['dateto'] = request.args.get('dateto')

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

        role, errors = role_schema.load(json_data, instance=role_obj, partial=True)
        if errors:
            logger.warning("Update role error", data=errors)
            return errors, 422
        # print(role)
        role.save()
        result = role_schema.dump(role).data
        return {'status': 'success', 'data': result}, 201
