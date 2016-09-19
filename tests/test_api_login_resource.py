#coding=utf-8

import unittest
import json
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.models import User

class ApiLoginResourceTestCase(unittest.TestCase):
    '''Test Api Login Resource'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.url = api.url_for(LoginResource)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }

    def test_login_resource_get(self):
        response = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
    
    def test_login_resource_post_valid(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response['token'])
        self.assertEqual(json_response['user']['username'],'test')
        self.assertEqual(json_response['user']['roles'],[])

    def test_login_resource_post_invalid_username(self):
        u = User(username='test', email='test@test.com')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'invalid', 'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message'],'Invalid username/password')

    def test_login_resource_post_invalid_password(self):
        u = User(username='test', email='test@test.com')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'password': 'invalid'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message'],'Invalid username/password')

    def test_login_resource_post_empty_args(self):
        response = self.client.post(self.url,
                                    data=json.dumps({}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['username'],'No username provided')

    def test_login_resource_post_no_username(self):
        response = self.client.post(self.url,
                                    data=json.dumps({'password': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['username'],'No username provided')

    def test_login_resource_post_no_password(self):
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code,400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['message']['password'],'No password provided')

    def test_login_resource_put(self):
        response = self.client.put(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_login_resource_delete(self):
        response = self.client.delete(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
