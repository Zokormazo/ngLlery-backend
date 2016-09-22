#coding=utf-8

import unittest
import json
from time import sleep
from app import create_app, db
from app.api import api
from app.api.resources.auth import LoginResource
from app.api.resources.gallery import AlbumPhotosListResource
from app.models import User, Album, Photo

class ApiAlbumPhotosListResourceTestCase(unittest.TestCase):
    '''Test Api AlbumPhotosList Resource '''

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

    def test_album_photos_list_resource_get_without_token(self):
        a = Album(path='/album')
        db.session.add(a)
        db.session.commit()
        album_id = a.id
        response = self.client.get(api.url_for(AlbumPhotosListResource,album_id=album_id), headers=self.get_headers())
        self.assertEqual(response.status_code,401)

    def test_album_photos_list_resource_get_with_valid_token(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        a = Album(path='/album')
        p1 = Photo(path='/photo1')
        p2 = Photo(path='/photo2')
        p3 = Photo(path='/photo3')
        a.photos.append(p1)
        a.photos.append(p2)
        a.photos.append(p3)
        db.session.add(u)
        db.session.add(a)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()
        album_id = a.id
        response = self.client.post(api.url_for(LoginResource),
                                    data=json.dumps({'username': 'test', 'password': 'test'}),
                                    headers=self.get_headers())
        json_data =  json.loads(response.data.decode('utf-8'))
        token = json_data['token']
        response = self.client.get(api.url_for(AlbumPhotosListResource,album_id=album_id), headers=self.get_headers(token))
        self.assertEqual(response.status_code,200)
        photos = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(photos),3)
        self.assertTrue('id' in photos[0])
        self.assertTrue('title' in photos[0])
        self.assertTrue('description' in photos[0])
        self.assertTrue('timestamp' in photos[0])
        self.assertFalse('path' in photos[0])
        self.assertFalse('created_at' in photos[0])

    def test_album_photos_list_resource_get_with_invalid_token(self):
        a = Album(path='/album')
        db.session.add(a)
        db.session.commit()
        album_id = a.id
        response = self.client.get(api.url_for(AlbumPhotosListResource,album_id=album_id), headers=self.get_headers(token='THIS_IS_AN_INVALID_TOKEN'))
        self.assertEqual(response.status_code,401)

    def test_album_photos_list_resource_post(self):
        response = self.client.post(api.url_for(AlbumPhotosListResource,album_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)

    def test_album_photos_list_resource_put(self):
        response = self.client.put(api.url_for(AlbumPhotosListResource,album_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)


    def test_album_photos_list_resource_delete(self):
        response = self.client.delete(api.url_for(AlbumPhotosListResource,album_id=0), headers=self.get_headers())
        self.assertEqual(response.status_code,405)
