"""API for Sample resource"""
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from app.models.sample import Sample, SampleSchema


api = Namespace('sample')
sample_schema = SampleSchema()
samples_schema = SampleSchema(many=True)


@api.route('/')
class List(Resource):
    """Sample list functionalities."""
    def get(self):
        """GET for Sample API"""
        all_samples = Sample.query.all()
        result = samples_schema.dump(all_samples)
        return jsonify({'meta': {}, 'objects': result.data})

    def post(self):
        """POST for Sample API"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        sample, errors = sample_schema.load(json_data)
        if errors:
            return errors, 422
        sample.save()
        result = sample_schema.dump(sample).data
        return result, 201


@api.route('/<uuid:uuid>/')
@api.response(404, 'Sample not found')
class Detail(Resource):
    """Sample details functionalities."""
    def get(self, uuid):
        """GET for Sample API Details"""
        sample = Sample.query.get(uuid)
        return sample_schema.jsonify(sample)
