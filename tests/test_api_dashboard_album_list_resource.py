#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.gallery import DashboardAlbumListResource
from app.models import User, Role, Album

class ApiDashboardAlbumListResourceTestCase(unittest.TestCase):
    '''Test Api DashboardAlbumList Resource '''

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.url = api.url_for(DashboardAlbumListResource)

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

    def test_dashboard_album_list_resource_get_without_token(self):
        response = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_dashboard_album_list_resource_get_with_valid_token(self):
        u = User(username='test', email='test@test.com')
        r = Role(name='admin')
        u.set_password('test')
        u.roles.append(r)
        a1 = Album(path='/album1')
        a2 = Album(path='/album2')
        a3 = Album(path='/album3')
        a4 = Album(path='/album4')
        db.session.add(u)
        db.session.add(r)
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.add(a4)
        db.session.commit()
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(self.url, headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        albums = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(albums),4)
        self.assertTrue('id' in albums[0])
        self.assertTrue('title' in albums[0])
        self.assertTrue('description' in albums[0])
        self.assertTrue('timestamp_from' in albums[0])
        self.assertTrue('timestamp_to' in albums[0])
        self.assertTrue('path' in albums[0])
        self.assertTrue('created_at' in albums[0])

    def test_dashboard_album_list_resource_get_with_invalid_token(self):
        response = self.client.get(self.url, headers=self.get_headers(token='THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_dashboard_album_list_resource_post(self):
        response = self.client.post(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_dashboard_album_list_resource_put(self):
        response = self.client.put(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_dashboard_album_list_resource_delete(self):
        response = self.client.delete(self.url, headers=self.get_headers())
        self.assertEqual(response.status_code,405)
