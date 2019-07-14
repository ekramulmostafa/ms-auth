# """Test related to Sample."""
# from flask import url_for
# from app.test import BaseTest
# from app.models.sample import Sample, SampleSchema
#
#
# class SampleApiTest(BaseTest):
#     """Test sample api"""
#     def setUp(self):
#         super().setUp()
#         obj = Sample(name="sample")
#         obj.save()
#         schema_response = SampleSchema().jsonify(obj)
#         self.sample_data = schema_response.json
#
#     def test_api_get(self):
#         """Test api get method."""
#         url = url_for('auth.sample_list')
#         response = self.client.get(url)
#         self.assert200(response)
#         self.assertEqual(response.json['objects'][0]['name'], self.sample_data['name'])
#         self.assertEqual(response.json['objects'][0]['id'], self.sample_data['id'])
#
#     def test_api_post(self):
#         """Test api post method."""
#         url = url_for('auth.sample_list')
#         response = self.client.post(
#             url,
#             json={
#                 'name': 'test-sample',
#             }
#         )
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json['name'], 'test-sample')
#
#     def test_api_detail(self):
#         """Test api detail method."""
#         url = url_for('auth.sample_detail', uuid=self.sample_data['id'])
#         response = self.client.get(url)
#         self.assert200(response)
#         self.assertEqual(response.json['name'], self.sample_data['name'])
#         self.assertEqual(response.json['id'], self.sample_data['id'])
