""" Role service """
from app.service.base_service import BaseService
from app.models.role import Role, RoleSchema

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class RoleService(BaseService):
    """ Role service """
    class Meta:
        """ 
            __searchable__ = fields in where checking the values
            __sortable__ = if use ! operator it will do desc operation else asc operation in the fields
            __filterable__ = fields for filtering ( operators are: rang(,) , >(_gt), <(_lt), >=(_gteq), <=(_lteq) . But for equals no need to use any operator, just (field = value) will be sufficent )
        """
        model = Role
        model_schema = role_schema
        models_schema = roles_schema
        # searchable = ['name']
        # sortable = ['id', '!created_at', 'updated_at']
        # filterable = ['active', 'created_at', 'updated_at']
