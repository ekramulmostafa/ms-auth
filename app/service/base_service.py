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
        results = self.__searchResults(results, values)
        results = self.__filterByResults(results, values)
        results = self.__orderByResults(results)
        results = self.__offsetLimit(results, values)
        results = results.all()

        return results

    def __offsetLimit(self, results, values):
        """ 
            results offset limit 
            limit and offset parameters needed for results to use limit, offset
        """
        limit = None
        offset = None
        if 'limit' in values and values['limit'] != None:
            limit = values['limit']
        if 'offset' in values and values['offset'] != None:
            offset = values['offset']

        if int(limit) > 0:
            results = results.limit(limit)

        if int(offset) > 0:
            results = results.offset(offset)
        return results

    def __searchResults(self, results, values):
        """ 
            search in searchable fields of the object 
            query_string parameter for search in searchable field(s)
        """
        Model = self.Meta.__model__
        if 'query_string' in values and values['query_string'] != None:
            value = values['query_string']
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
            if (val != None and val != 0 and val != "") and self.__filterableFieldChecking(filterable, key):
                results = results.filter(self.__expressionReturn(Model, key, val))

        return results

    def __filterableFieldChecking(self, filterable, key_value_pair):
        """ filterableFieldChecking """

        for field in filterable:
            if key_value_pair == field:
                return True
        return False

    def __expressionReturn(self, Model, field, val):
        """
            filter fields of the object
        """
        expression = None
        if val.find(',') > 0:
            arr = val.split(',')
            # print(arr)
            expression = Model.__dict__[field].between(arr[0], arr[1])

        elif val.find('_') > 0:
            arr = val.split('_')
            operator = arr[1]
            value = arr[0]
            if operator == "gt" and field in Model.__dict__:
                expression = Model.__dict__[field] > value

            elif operator == "gteq" and field in Model.__dict__:
                expression = Model.__dict__[field] >= value

            elif operator == "lt" and field in Model.__dict__:
                expression = Model.__dict__[field] < value

            elif operator == "lteq" and field in Model.__dict__:
                expression = Model.__dict__[field] <= value

        else:
            expression = Model.__dict__[field] == val

        return expression
