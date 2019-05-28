""" Role service """
from app.service.base_service import BaseService
from app.models.role import Role


class RoleService(BaseService):
    """ Role service """
    class Meta:
        """ 
            __searchable__ = fields in where checking the values
            __sortable__ = if use ! operator it will do desc operation else asc operation in the fields
            __filterable__ = fields for filtering ( operators are: rang(,) , >(_gt), <(_lt), >=(_gteq), <=(_lteq) . But for equals no need to use any operator, just (field = value) will be sufficent )
        """
        __model__ = Role
        __searchable__ = ['name']
        __sortable__ = ['id', '!created_at', 'updated_at']
        __filterable__ = ['active', 'created_at', 'updated_at']
