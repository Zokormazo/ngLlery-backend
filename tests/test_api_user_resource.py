#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.users import UserResource
from app.models import User

class ApiUserResourceTestCase(unittest.TestCase):
    '''Test Api User Resource '''

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
            'Content-type': 'application/json',
            'Authorization': token
        }

    def test_user_resource_get_without_token(self):
        response = self.client.get(api.url_for(UserResource,user_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_user_resource_get_with_valid_token_and_valid_user_id(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        user_id = json_data['user']['id']
        response = self.client.get(api.url_for(UserResource,user_id=user_id), headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        user = json.loads(response.data.decode('utf-8'))['user']
        self.assertEqual(user['username'],'test')
        self.assertFalse('email' in user)
        self.assertTrue('registered_at' in user)
        self.assertTrue('last_seen' in user)
        self.assertTrue('id' in user)
        self.assertTrue('roles' in user)

    def test_user_resource_get_with_valid_token_and_invalid_user_id(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        user_id = json_data['user']['id']
        response = self.client.get(api.url_for(UserResource,user_id=user_id+1), headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_user_resource_get_with_invalid_token(self):
        response = self.client.get(api.url_for(UserResource,user_id=0), headers=self.get_headers(token='THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_user_resource_get_with_expired_token(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        self.app.config['AUTH_TOKEN_EXPIRATION_TIME'] = 1
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data = json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        sleep(2)
        response = self.client.get(api.url_for(UserResource,user_id=0), headers=self.get_headers(token))
        self.assertEqual(response.status_code,401)

    def test_user_resource_post(self):
        response = self.client.post(api.url_for(UserResource,user_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_user_resource_put(self):
        response = self.client.put(api.url_for(UserResource,user_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_user_resource_delete(self):
        response = self.client.delete(api.url_for(UserResource,user_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)
