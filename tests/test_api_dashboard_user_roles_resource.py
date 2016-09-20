#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.users import DashboardUserRolesResource
from app.models import User,Role

class ApiDashboardUserRolesResourceTestCase(unittest.TestCase):
    '''Test Api DashboardUserRoles Resource '''

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

    def test_dashboard_user_roles_resource_get(self):
        response = self.client.get(api.url_for(DashboardUserRolesResource,user_id=0,role_name='Role'), headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_dashboard_user_roles_resource_post_without_token(self):
        response = self.client.post(api.url_for(DashboardUserRolesResource, user_id=0, role_name='Role'), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_roles_resource_post_with_valid_token_and_role_and_valid_user_id_and_role_name(self):
        r = Role(name='admin')
        r1 = Role(name='poweruser')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        db.session.add(r)
        db.session.add(r1)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        user_id = json_data['user']['id']
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=user_id, role_name='poweruser'),
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,204)

    def test_dashboard_user_roles_resource_post_with_valid_token_and_role_and_valid_user_id_but_invalid_role_name(self):
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
        user_id = json_data['user']['id']
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=user_id, role_name='Role'),
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_dashboard_user_roles_resource_post_with_valid_token_and_role_and_invalid_user_id_and_valid_role_name(self):
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
        user_id = json_data['user']['id']
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=user_id+1, role_name='admin'),
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_dashboard_user_roles_resource_post_with_valid_token_and_role_and_invalid_user_id_and_role_name(self):
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
        user_id = json_data['user']['id']
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=user_id+1, role_name='Role'),
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_dashboard_user_roles_resource_post_with_valid_token_but_without_role(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=0, role_name='Role'), headers=self.get_headers(token))
        self.assertEqual(response.status_code,403)

    def test_dashboard_user_roles_resource_post_with_invalid_token(self):
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=0,role_name='Role'), headers=self.get_headers('THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_roles_resource_post_with_expired_token(self):
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
        response = self.client.post(api.url_for(DashboardUserRolesResource,user_id=0,role_name='Role'), headers=self.get_headers(token))
        self.assertEqual(response.status_code,401)

    def test_dashboard_user_roles_resource_put(self):
        response = self.client.put(api.url_for(DashboardUserRolesResource,user_id=0,role_name='Role'), headers=self.get_headers())
        self.assertEqual(response.status_code,405)
