#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.gallery import DashboardPhotoResource
from app.models import User, Role, Photo

class ApiDashboardPhotoResourceTestCase(unittest.TestCase):
    '''Test Api DashboardPhoto Resource '''

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

    def test_dashboard_photo_resource_get_without_token(self):
        response = self.client.get(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_photo_resource_get_with_valid_token_and_role_and_valid_photo_id(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        p = Photo(path='/photo')
        db.session.add(r)
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        photo_id=p.id
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(api.url_for(DashboardPhotoResource,photo_id=photo_id), headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        photo = json.loads(response.data.decode('utf-8'))
        self.assertEqual(photo['path'],'/photo')
        self.assertTrue('title' in photo)
        self.assertTrue('description' in photo)
        self.assertTrue('id' in photo)
        self.assertTrue('timestamp' in photo)

    def test_dashboard_photo_resource_get_with_valid_token_and_role_and_invalid_photo_id(self):
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
        response = self.client.get(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_dashboard_photo_resource_get_with_valid_token_but_without_role(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers(token))
        self.assertEqual(response.status_code,403)

    def test_dashboard_photo_resource_get_with_invalid_token(self):
        response = self.client.get(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers('THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_photo_resource_post_without_token(self):
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_photo_resource_post_with_valid_token_and_role_and_valid_photo_id_without_data(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        p = Photo(path='/photo')
        db.session.add(r)
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        photo_id = p.id
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=photo_id),
                                    data=json.dumps({}),
                                    headers=self.get_headers(token))
        self.assertEqual(response.status_code,204)

    def test_dashboard_photo_resource_post_with_valid_token_and_role_and_valid_photo_id_with_valid_data(self):
        r = Role(name='admin')
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        u.roles.append(r)
        p = Photo(path='/photo')
        db.session.add(r)
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        photo_id = p.id
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        user_id = json_data['user']['id']
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=photo_id),
                                    data=json.dumps({'title': 'title',
                                                     'description': 'description',
                                                     'timestamp': 'Wed, 02 Oct 2002 13:00:00 GMT'}),
                                    headers=self.get_headers(token))
        print response.data
        self.assertEqual(response.status_code,204)


    def test_dashboard_photo_resource_post_with_valid_token_and_role_and_invalid_photo_id(self):
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
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers(token))
        self.assertEqual(response.status_code,404)

    def test_dashboard_photo_resource_post_with_valid_token_but_without_role(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        db.session.add(u)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers(token))
        self.assertEqual(response.status_code,403)

    def test_dashboard_photo_resource_post_with_invalid_token(self):
        response = self.client.post(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers('THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_photo_resource_delete(self):
        response = self.client.delete(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_dashboard_photo_resource_put(self):
        response = self.client.put(api.url_for(DashboardPhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)
