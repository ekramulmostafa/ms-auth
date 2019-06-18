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

    def offset_limit(self, results, values):
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

    def order_by_results(self, results):
        """ order by results """

        model = self.Meta.model
        sortable = self.Meta.sortable

        for field in sortable:
            if field.find('!') == 0:
                field = field.lstrip('!')
                if field in model.__dict__:
                    results = results.order_by(desc(model.__dict__[field]))
            else:
                if field in model.__dict__:
                    results = results.order_by(model.__dict__[field])

        return results

    def filter_by_results(self, results, values):
        """ fitler by results """
        model = self.Meta.model
        filterable = self.Meta.filterable

        for key, val in values.items():
            if (val is not None and val != 0) and self.__filterable_field_checking(filterable, key):
                results = results.filter(self.__expression_return(model, key, val))

        return results

    @staticmethod
    def __filterable_field_checking(filterable, key_value_pair):
        """ filterableFieldChecking """

        for field in filterable:
            if key_value_pair == field:
                return True
        return False

    @staticmethod
    def __expression_return(model, field, val):
        """
            filter fields of the object
        """
        expression = None
        if val.find(',') > 0:
            arr = val.split(',')
            # print(arr)
            expression = model.__dict__[field].between(arr[0], arr[1])

        elif val.find('_') > 0:
            arr = val.split('_')
            operator = arr[1]
            value = arr[0]
            if operator == "gt" and field in model.__dict__:
                expression = model.__dict__[field] > value

            elif operator == "gteq" and field in model.__dict__:
                expression = model.__dict__[field] >= value

            elif operator == "lt" and field in model.__dict__:
                expression = model.__dict__[field] < value

            elif operator == "lteq" and field in model.__dict__:
                expression = model.__dict__[field] <= value

        else:
            expression = model.__dict__[field] == val

        return expression

    def get_by_uuid(self, uuid):
        """ get by uuid """
        model = self.Meta.model

        results = model.query.get(uuid)
        return results

    def get_by_values(self, values):
        """ get by values """
        model = self.Meta.model

        results = model.query
        results = self.filter_by_results(results, values)
        results = self.order_by_results(results)
        results = self.offset_limit(results, values)

        results = results.all()

        return results

    def fetch(self, uuid=None, values=None):
        """ Get """
        if uuid:
            result = self.get_by_uuid(uuid)
            result = self.Meta.model_schema.dump(result).data
            return result

        results = self.get_by_values(values)
        results = self.Meta.models_schema.dump(results)
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
        model = self.Meta.model
        schema = self.Meta.model_schema

        model_query = model.query.get(uuid)
        if model_query is None:
            return {'message': 'Content not found'}, 404

        model_instance, errors = schema.load(json_data, instance=model_query, partial=True)
        if errors:
            return errors, 422

        model_instance.save()
        result = schema.dump(model_instance).data

        return result
