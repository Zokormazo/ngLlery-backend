#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.gallery import PhotoResource
from app.models import User, Photo

class ApiPhotoResourceTestCase(unittest.TestCase):
    '''Test Api Photo Resource '''

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

    def test_photo_resource_get_without_token(self):
        response = self.client.get(api.url_for(PhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_photo_resource_get_with_valid_token(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        p = Photo(path='/photo')
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        photo_id = p.id
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(api.url_for(PhotoResource,photo_id=photo_id), headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        album = json.loads(response.data.decode('utf-8'))
        self.assertTrue('id' in album)
        self.assertTrue('title' in album)
        self.assertTrue('description' in album)
        self.assertTrue('timestamp' in album)
        self.assertFalse('path' in album)
        self.assertFalse('created_at' in album)

    def test_photo_resource_get_with_invalid_token(self):
        response = self.client.get(api.url_for(PhotoResource,photo_id=0), headers=self.get_headers(token='THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_photo_resource_post(self):
        response = self.client.post(api.url_for(PhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_photo_resource_put(self):
        response = self.client.put(api.url_for(PhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_photo_resource_delete(self):
        response = self.client.delete(api.url_for(PhotoResource,photo_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)
