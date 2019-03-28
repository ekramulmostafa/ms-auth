""" Test permission api"""
import json
from flask import url_for
from app.test import BaseTest
from app.models.permission import Permission, PermissionSchema


class PemissionTests(BaseTest):
    """ Permission Test api class"""

    def setUp(self):
        super().setUp()
        obj = Permission(code='codeStr0159', name='codeStr0159',
                         active=True)
        obj.save()
        schema_response = PermissionSchema().jsonify(obj)
        self.permission_data = schema_response.json

    def test_get(self):
        """ Permission get call
        Permission search call
        Permission filter call
        Permission limit & offset
        """
        url = url_for('auth.permission_permission_list')
        response = self.client.get(
            url,
            content_type='application/json'
        )
        self.assert200(response)
        search_var = {'search': 'cssfdf'}
        search_url = url_for('auth.permission_permission_list', **search_var)

        response = self.client.get(
            search_url,
            content_type='application/json'
        )
        self.assert200(response)
        active_var = {'active': True}
        active_url = url_for('auth.permission_permission_list', **active_var)
        response = self.client.get(
            active_url,
            content_type='application/json'
        )
        self.assert200(response)
        offset_var = {'limit': 1, 'offset': 1}
        offset_url = url_for('auth.permission_permission_list', **offset_var)
        response = self.client.get(
            offset_url,
            content_type='application/json'
        )
        self.assert200(response)

    def test_post_and_put(self):
        """ test post call"""
        url = url_for('auth.permission_permission_list')
        response = self.client.post(
            url,
            data=json.dumps(dict(
                code='codeStr0160',
                name='codeStr0160cle',
                active=True
            )),
            content_type='application/json'
        )
        json_response = json.loads(response.get_data(as_text=True))
        put_url = url_for('auth.permission_permission_detail', uuid=json_response['data']['id'])
        self.assertEqual(response.status_code, 201)
        response = self.client.put(
            put_url,
            data=json.dumps(dict(
                active=True
            )),
            content_type='application/json'
        )
        self.assert200(response)
        response = self.client.get(
            put_url,
            content_type='application/json'
        )
        self.assert200(response)
