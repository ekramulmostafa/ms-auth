""" Base service """


class BaseService:
    """ class base service 
        1. __searchable__ = type array
        2. __sortable__ = type array
        3. __filterable__ = type array
        4. __model__ = type string
    """
    __abstract__ = True

    def get_all(self):
        """ """
