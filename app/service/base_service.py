""" Base service """
from sqlalchemy import desc, or_, and_


class BaseService:
    """ class base service
        1. __searchable__ = type array
        2. __sortable__ = type array
        3. __filterable__ = type array
        4. __model__ = type Model
    """
    __abstract__ = True

    def get_all(self, values):
        """ Get all """

        Model = self.Meta.__model__
        # print(Model)
        results = Model.query
        results = self.__searchResults(results, values['query_string'])
        results = self.__offsetLimit(results, values['limit'], values['offset'])
        results = self.__orderByResults(results)
        results = self.__filterByResults(results, values)
        results = results.all()

        return results

    def __offsetLimit(self, results, limit, offset):
        """ results offset limit """
        if limit != None and int(limit) > 0:
            results = results.limit(limit)

        if limit != None and int(offset) > 0:
            results = results.offset(offset)
        return results

    def __searchResults(self, results, value):
        """ search in searchable fields of the object """
        Model = self.Meta.__model__
        if value != None:
            for field in self.Meta.__searchable__:
                if field in Model.__dict__:
                    results = results.filter(Model.__dict__[field].like("%" + value + "%"))
        return results

    def __orderByResults(self, results):
        """ order by results """
        Model = self.Meta.__model__
        sortable = self.Meta.__sortable__

        for field in sortable:
            if field.find('!') == 0:
                field = field.lstrip('!')
                if field in Model.__dict__:
                    results = results.order_by(desc(Model.__dict__[field]))
            else:
                if field in Model.__dict__:
                    results = results.order_by(Model.__dict__[field])

        return results

    def __filterByResults(self, results, values):
        """ fitler by results """
        Model = self.Meta.__model__
        filterable = self.Meta.__filterable__

        for key, val in values.items():
            if (val != None and val != 0 and val != "") and self.__filterableFieldChecking(key):
                if val.find(','):
                    pass
                elif val.find('_'):
                    pass
                print(key, val)

        return results

    def __filterableFieldChecking(self, key_value_pair):
        """ filterableFieldChecking """
        print("key value pair")
        print(key_value_pair)
        filterable = self.Meta.__filterable__
        for field in filterable:
            if key_value_pair == field:
                return True
        return False
