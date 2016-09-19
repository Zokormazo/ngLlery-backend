#coding=utf-8

import unittest
import json
from flask import current_app
from app import create_app
from app.api import api
from app.api.resources.config import ConfigResource

class ApiConfigResourceTestCase(unittest.TestCase):
    '''Test Api Config Resource'''

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.url = api.url_for(ConfigResource)

    def tearDown(self):
        self.app_context.pop()

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }

    def test_config_resource_get(self):
        current_app.config['SITE_NAME'] = 'Test Site Name'
        current_app.config['SITE_DESCRIPTION'] = 'Test Site Description'
        current_app.config['AUTH_TOKEN_EXPIRATION_TIME'] = 600
        current_app.config['AUTH_TOKEN_ENABLE_REGISTRATION'] = True
        response = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['config']['info']['name'],'Test Site Name')
        self.assertEqual(json_response['config']['info']['description'],'Test Site Description')
        self.assertEqual(json_response['config']['auth']['tokenExpirationTime'],600)
        self.assertEqual(json_response['config']['auth']['enableRegistration'],True)

    def test_config_resource_post(self):
        response = self.client.post(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_config_resource_put(self):
        response = self.client.put(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_config_resource_delete(self):
        response = self.client.delete(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
