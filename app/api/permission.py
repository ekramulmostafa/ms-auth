""" API for permission resource """
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.models.permission import PermissionModel, PermissionSchema
from sqlalchemy import desc,asc


api = Namespace('permission')
permission_schema =  PermissionSchema()
permissions_schema = PermissionSchema(many=True)
permission_model = api.model('post a permission',{"name":fields.String(description="name of permission", required=True),"code":fields.String(description="code of permission", required=True),"active":fields.Boolean(description="status of permission", required=True)})

@api.route('')
class Permission(Resource):
    def get(self):
        """this api will return list of permission with filter options ?search=value&sort_by=field_name&limit=10&offset=0&order_by=desc/asc&field_name=value"""
        all_permission  = PermissionModel.get_permission(self, **request.args)
        result =  permissions_schema.dump(all_permission)
        return jsonify({"status":"success","data" : result.data})

    @api.expect(permission_model)
    def post(self):
        """ post a permission """
        json_data =  request.get_json()
        if not json_data:
            return {'status': 'failed','result': "No json data is found"}, 400
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
        result = permission_schema.dump(permission)
        return jsonify({"status":"success","data" :result.data})

    def patch(self, uuid):
        """ update permission"""
        permission_info = PermissionModel.query.get(uuid)
        if not permission_info:
            return {'status': 'failed',"result" : "Permission uuid is not valid!"}, 400
        json_data =  request.get_json()
        json_data['id'] = uuid
        if not json_data:
            return {'status': 'failed',"result" :  "No data to update"},400
        #serializer & validation
        permission_data, error = permission_schema.load(json_data,partial=True)
        if error:
            return error, 400
        result = permission_data.save()
        
        return {'status':'success','data': result}, 200


        
        
       


