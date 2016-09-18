#coding=utf8

import unittest
import json
from flask import current_app
from app import create_app, db
from app.api import api
from app.api.resources.config import ConfigResource
from app.api.resources.auth import LoginResource, RegisterResource
from app.models import User

class ApiTestCase(unittest.TestCase):
    '''test api'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_headers(self, token=''):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
    
    def test_404(self):
        response = self.client.get('/wrong-url', headers=self.get_headers())
        self.assertTrue(response.status_code == 404)

    def test_config_resource(self):
        response = self.client.get(api.url_for(ConfigResource), headers=self.get_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['config']['info']['name'] == current_app.config['SITE_NAME'])
        self.assertTrue(json_response['config']['info']['description'] == current_app.config['SITE_DESCRIPTION'])
        self.assertTrue(json_response['config']['auth']['tokenExpirationTime'] == current_app.config['AUTH_TOKEN_EXPIRATION_TIME'])
        self.assertTrue(json_response['config']['auth']['enableRegistration'] == current_app.config['AUTH_ENABLE_REGISTRATION'])

    def test_login_resource(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertTrue(response.status_code == 200)
        response2 = self.client.post(api.url_for(LoginResource),
                                     data=json.dumps({'username': 'test', 'password': 'wrong'}),
                                     headers=self.get_headers())
        self.assertTrue(response2.status_code == 400)        
        response3 = self.client.post(api.url_for(LoginResource),
                                     headers = self.get_headers())

    def test_register_resource(self):
        data = json.dumps({'username': 'test', 'email': 'test@test.com', 'password': 'test'})
        response = self.client.post(api.url_for(RegisterResource),
                                    data=data,
                                    headers=self.get_headers())
        self.assertTrue(response.status_code == 201)
        response2 = self.client.post(api.url_for(RegisterResource),
                                     data=data,
                                     headers=self.get_headers())
        self.assertTrue(response2.status_code == 400)
