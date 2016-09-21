#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.users import DashboardUserListResource
from app.models import User,Role

class ApiDashboardUserListResourceTestCase(unittest.TestCase):
    '''Test Api DashboardUserList Resource '''

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.url = api.url_for(DashboardUserListResource)

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

    def test_dashboard_user_list_resource_get_without_token(self):
        response = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_list_resource_get_with_valid_token_and_role(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        u1 = User(username='foo', email='foo@foo.com')
        u2 = User(username='bar', email='bar@bar.com')
        db.session.add(r)
        db.session.add(u)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(self.url, headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        users = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(users),3)
        self.assertEqual(users[0]['username'],'test')
        self.assertEqual(users[1]['username'],'foo')
        self.assertEqual(users[2]['username'],'bar')        
        self.assertTrue('email' in users[0])
        self.assertTrue('registered_at' in users[0])
        self.assertTrue('last_seen' in users[0])
        self.assertTrue('id' in users[0])
        self.assertTrue('roles' in users[0])

    def test_dashboard_user_list_resource_get_with_valid_token_but_without_role(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(self.url, headers=self.get_headers(token))
        self.assertEqual(response.status_code,403)

    def test_dashboard_user_list_resource_get_with_invalid_token(self):
        response = self.client.get(self.url, headers=self.get_headers('THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_list_resource_post_without_token(self):
        response = self.client.post(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_valid_data(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test2', 'password': 'test2', 'email': 'test2@test.com'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_empty_data(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_no_username(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'password': 'test2', 'email': 'test2@test.com'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_no_password(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test2', 'email': 'test2@test.com'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_no_email(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test2', 'password': 'test2'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_duplicated_username(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test', 'password': 'test2', 'email': 'test2@test.com'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_and_role_and_duplicated_email(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url,
                                    data=json.dumps({'username': 'test2', 'password': 'test2', 'email': 'test@test.com'}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,400)

    def test_dashboard_user_list_resource_post_with_valid_token_but_without_role(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data = json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(self.url, headers=self.get_headers(token))
        self.assertEqual(response.status_code,403)

    def test_dashboard_user_list_resource_post_with_invalid_token(self):
        response = self.client.post(self.url, headers=self.get_headers('THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_list_resource_put(self):
        response = self.client.put(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_dashboard_user_list_resource_delete(self):
        response = self.client.delete(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
