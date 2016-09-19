#coding=utf-8

import unittest
import json
from flask import current_app
from app import create_app, db
from app.api import api
from app.api.resources.auth import RegisterResource
from app.models import User

class ApiRegisterResourceTestCase(unittest.TestCase):
    '''Test Api Register Resource'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.url = api.url_for(RegisterResource)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }

    def test_register_resource_get(self):
        response = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_register_resource_post_disabled_registration(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = False
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message'],'user registration disabled')

    def test_register_resource_post_valid(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,201)

    def test_register_resource_post_duplicated_username(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test2@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message'],'username or email already exists')

    def test_register_resource_post_duplicated_email(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test2', 'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message'],'username or email already exists')

    def test_register_resource_post_missing_username(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'email': 'test@test.com', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['username'],'No username provided')

    def test_register_resource_post_missing_email(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['email'],'No email provided')

    def test_register_resource_post_missing_password(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'email': 'test@test.com'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['password'],'No password provided')

    def test_register_resource_post_empty_args(self):
        current_app.config['AUTH_ENABLE_REGISTRATION'] = True
        response = self.client.post(self.url,
                                    data=json.dumps({}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['username'],'No username provided')
        
    def test_register_resource_put(self):
        response = self.client.put(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_register_resource_delete(self):
        response = self.client.delete(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
