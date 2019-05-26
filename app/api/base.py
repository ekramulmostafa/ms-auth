from flask_restplus import Resource
from flask import request


class BaseResource(Resource):
    __abstract__ = True


class ResourceAll(BaseResource):
    def get(self):
        print("GET")
        pass

    def post(self):
        data = request.json
        print(data)
        pass


class ResourceDetails(BaseResource):
    def get(self, value):
        print(value)
        pass
