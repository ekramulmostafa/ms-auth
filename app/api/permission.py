""" API for permission resource """
import sys
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from sqlalchemy.exc import ProgrammingError
from app.models.permission import PermissionModel, PermissionSchema


api = Namespace('permission')
permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)


@api.route('')
class Permission(Resource):
    """ Permission Resource """

    def get(self):
        """this api will return list of permission with filter options
        ?search=value&sort_by=field_name&limit=10&offset=0&order_by=desc/asc&field_name=value"""
        try:
            all_permission = PermissionModel.get_permission(self, **request.args)
            result = permissions_schema.dump(all_permission)
            return jsonify({"status": "success", "data": result.data})
        except ProgrammingError:
            e = "Oops!", sys.exc_info()[0], "occured."
            return {"status": "error", "error": str(e)}, 500

    # @api.expect(permission_model)
    def post(self):
        """ post a permission """
        try:
            json_data = request.get_json()
            if not json_data:
                return {'status': 'failed', 'result': "No json data is found"}, 400
            permission_data, error = permission_schema.load(json_data)
            if error:
                return error, 400
            permission_data.save()
            result = permission_schema.dump(permission_data).data
            return {'status': 'success', 'data': result}, 200
        except ProgrammingError:
            e = "Oops!", sys.exc_info()[0], "occured."
            return {"status": "error", "error": str(e)}, 500


@api.route('/<uuid:uuid>/')
@api.response(404, 'Permission not found')
class PermissionDetail(Resource):

    """Get Permission details."""

    def get(self, uuid):
        """GET permission API Details"""
        try:
            permission = PermissionModel.query.get(uuid)
            result = permission_schema.dump(permission)
            return jsonify({"status": "success", "data": result.data})
        except ProgrammingError:
            e = "Oops!", sys.exc_info()[0], "occured."
            return {"status": "error", "error": str(e)}, 500

    def put(self, uuid):
        """ update permission"""
        try:
            permission_info = PermissionModel.query.get(uuid)
            if not permission_info:
                return {'status': 'failed', "result": "Permission uuid is not valid!"}, 400
            json_data = request.get_json()
            json_data['id'] = uuid
            if not json_data:
                return {'status': 'failed', "result":  "No data to update"}, 400
            permission_data, error = permission_schema.load(json_data, partial=True)
            if error:
                return error, 400
            permission_data.save()
            return {'status': 'success', 'data': permission_schema.dump(permission_data).data}, 200
        except ProgrammingError:
            e = "Oops!", sys.exc_info()[0], "occured."
            return {"status": "error", "error": str(e)}, 500
