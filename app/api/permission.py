""" API for permission resource """
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.models.permission import PermissionModel, PermissionSchema
from sqlalchemy import desc,asc

api = Namespace('permission')
permission_schema =  PermissionSchema()
permissions_schema = PermissionSchema(many=True)

@api.route('')
class Permission(Resource):
    def get(self):
        all_permission  = PermissionModel.get_permission(request.args,**request.args)
        result =  permissions_schema.dump(all_permission)
        return jsonify(result.data)

    def post(self):
        """ post a permission """
        json_data =  request.get_json()
        if not json_data:
            return {'result': "no post data"}, 400
        #serilizer & validation
        permission_data, error = permission_schema.load(json_data)
        if error:
            return error, 400
        permission_data.save()
        result = permission_schema.dump(permission_data).data
        return {'status': 'success', 'data': result}, 200



@api.route('/<uuid:uuid>/')
@api.response(404, 'Permission not found')
class PermissionDetail(Resource):
    """Get Permission details."""
    def get(self, uuid):
        """GET permission API Details"""
        permission = PermissionModel.query.get(uuid)
        return permission_schema.jsonify(permission)

    def patch(self, uuid):
        """ update permission"""
        permission_info = PermissionModel.query.get(uuid)
        if not permission_info:
            return {"result" : "Permission id is not valid!"}, 400
        json_data =  request.get_json()
        json_data['id'] = uuid
        if not json_data:
            return {"result" :  "No data to update"},400
        #serializer & validation
        permission_data, error = permission_schema.load(json_data,partial=True)
        if error:
            return error, 400
        result = permission_data.save()
        
        return {'result': result}, 200


        
        
       


