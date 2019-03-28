""" API for permission resource """

from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.logging import Logger
from app.models.permission import Permission, PermissionSchema


api = Namespace('permission')
permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)

logger = Logger(__name__)


@api.route('')
class PermissionList(Resource):
    """ Permission Resource """

    def get(self):
        """this api will return list of permission with filter options
        ?search=value&sort_by=field_name&limit=10&offset=0&order_by=desc/asc&field_name=value"""
        all_permission = Permission.get_permission(self, **request.args)
        result = permissions_schema.dump(all_permission)
        return jsonify({"status": "success", "data": result.data})

    # @api.expect(permission_model)
    def post(self):
        """ post a permission """
        json_data = request.get_json()
        if not json_data:
            return {'status': 'failed', 'result': "No json data is found"}, 400
        permission_data, error = permission_schema.load(json_data)
        if error:
            logger.warning("Validation failed", data=error)
            return error, 422
        permission_data.save()
        result = permission_schema.dump(permission_data).data
        return {'status': 'success', 'data': result}, 201


@api.route('/<uuid:uuid>/')
@api.response(404, 'Permission not found')
class PermissionDetail(Resource):

    """Get Permission details."""

    def get(self, uuid):
        """GET permission API Details"""
        permission = Permission.query.get(uuid)
        result = permission_schema.dump(permission)
        return jsonify({"status": "success", "data": result.data})

    def put(self, uuid):
        """ update permission"""
        permission_info = Permission.query.get(uuid)
        if not permission_info:
            return {'status': 'failed', "result": "Permission uuid is not valid!"}, 400
        json_data = request.get_json()
        if not json_data:
            return {'status': 'failed', "result":  "No data to update"}, 400
        permission_data, error = permission_schema.load(
            json_data, instance=permission_info, partial=True
        )
        if error:
            logger.warning("Validation failed", data=error)
            return error, 422
        permission_data.save()
        return {'status': 'success', 'data': permission_schema.dump(permission_data).data}, 200
