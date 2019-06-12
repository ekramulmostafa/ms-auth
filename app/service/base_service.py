""" Base service """
from sqlalchemy import desc


class BaseService:
    """ class base service
        1. __searchable__ = type array
        2. __sortable__ = type array
        3. __filterable__ = type array
        4. __model__ = type Model
    """
    __abstract__ = True

    class Meta:
        """ Meta base service """
        model = None
        model_schema = None
        models_schema = None
        sortable = []
        filterable = []

    def __init__(self, **kwargs):
        """ initiate base service """
        self.Meta.sortable = kwargs.get('sortable')
        self.Meta.filterable = kwargs.get('filterable')

    def offsetLimit(self, results, values):
        """ results offset limit
            limit and offset parameters needed for results to use limit, offset """

        limit = None
        offset = None
        if 'limit' in values and values['limit'] is not None:
            limit = values['limit']
        if 'offset' in values and values['offset'] is not None:
            offset = values['offset']

        if int(limit) > 0:
            results = results.limit(limit)

        if int(offset) > 0:
            results = results.offset(offset)
        return results

    def orderByResults(self, results):
        """ order by results """

        Model = self.Meta.model
        sortable = self.Meta.sortable

        for field in sortable:
            if field.find('!') == 0:
                field = field.lstrip('!')
                if field in Model.__dict__:
                    results = results.order_by(desc(Model.__dict__[field]))
            else:
                if field in Model.__dict__:
                    results = results.order_by(Model.__dict__[field])

        return results

    def filterByResults(self, results, values):
        """ fitler by results """
        Model = self.Meta.model
        filterable = self.Meta.filterable

        for key, val in values.items():
            if (val is not None and val != 0) and self.__filterableFieldChecking(filterable, key):
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

    def fetch(self, uuid=None, values=None):
        """ Get """
        if uuid:
            result = self.getByUUID(uuid)
            result = self.Meta.model_schema.dump(result).data
            return result

        results = self.getByValues(values)
        results = self.Meta.models_schema.dump(results)
        return results

    def getByUUID(self, uuid):
        """ get by uuid """
        Model = self.Meta.model

        results = Model.query.get(uuid)
        return results

    def getByValues(self, values):
        """ get by values """
        Model = self.Meta.model

        results = Model.query
        results = self.filterByResults(results, values)
        results = self.orderByResults(results)
        results = self.offsetLimit(results, values)

        results = results.all()

        return results

    def create(self, json_data):
        """ Post """
        schema = self.Meta.model_schema
        instance, errors = schema.load(json_data)
        if errors:
            return errors, 422
        instance.save()
        result = schema.dump(instance).data
        return result

    def update(self, uuid=None, json_data=None):
        """ update """
        Model = self.Meta.model
        schema = self.Meta.model_schema

        model_query = Model.query.get(uuid)
        if model_query is None:
            return {'message': 'Content not found'}, 404

        model_instance, errors = schema.load(json_data, instance=model_query, partial=True)
        if errors:
            return errors, 422

        model_instance.save()
        result = schema.dump(model_instance).data

        return result
