""" Base service """
from sqlalchemy import desc


class BareboneBaseService:
    """ BareboneBaseService Base Service """
    __abstract__ = True

    class Meta:
        """ Meta base service """
        model = None
        model_schema = None
        models_schema = None
        sortable = []
        filterable = []

    def fetch(self, uuid=None, values=None):
        """ Get """

    def create(self, json_data):
        """ Post """

    def update(self, uuid=None, json_data=None):
        """ update """


class BaseService(BareboneBaseService):
    """ class base service
        1. __searchable__ = type array
        2. __sortable__ = type array
        3. __filterable__ = type array
        4. __model__ = type Model
    """

    # def __init__(self, sortable=[], filterable=[]):
    def __init__(self):
        """ initiate base service """
        self.model = self.Meta.model

    def __call__(self, sortable=[], filterable=[]):
        """ call function """
        self.sortable = sortable
        self.filterable = filterable

    @staticmethod
    def offset_limit(results, values):
        """ results offset limit
            limit and offset parameters needed for results to use limit, offset """

        limit = 0
        offset = 0
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

        for field in self.sortable:
            if field.find('!') == 0:
                field = field.lstrip('!')
                if field in self.model.__dict__:
                    results = results.order_by(desc(self.model.__dict__[field]))
            else:
                if field in self.model.__dict__:
                    results = results.order_by(self.model.__dict__[field])

        return results

    def filter_by_results(self, results, values):
        """ fitler by results """

        for key, val in values.items():
            if (val is not None and val != 0) \
                    and self.__filterable_field_checking(self.filterable, key):
                results = results.filter(self.__expression_return(self.model, key, val))

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
        results = self.model.query.get(uuid)
        return results

    def get_by_values(self, values=None):
        """ get by values """
        results = self.model.query
        if values is not None:
            results = self.filter_by_results(results, values)
            results = self.order_by_results(results)
            results = self.offset_limit(results, values)

        results = results.all()

        return results

    def fetch(self, uuid=None, values=None):
        """ Get """
        if uuid:
            result = self.get_by_uuid(uuid)
            return result

        results = self.get_by_values(values)
        return results

    @staticmethod
    def save_instance(instance):
        """ save instance """
        instance.save()
        return instance

    def perform_create(self, instance):
        """ perform create """
        return self.save_instance(instance)

    def perform_update(self, instance):
        """ perform update """
        return self.save_instance(instance)
