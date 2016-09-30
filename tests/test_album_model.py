#coding=utf8

import unittest

from app import create_app, db
from app.models import Album, Photo

class AlbumModelTestCase(unittest.TestCase):
    '''test album model'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_children_count(self):
        album1 = Album(path='/test1')
        album2 = Album(path='/test2')
        photo1 = Photo(path='/test1/photo1.jpg', album=album1)
        photo2 = Photo(path='/test1/photo2.jpg', album=album1)
        photo3 = Photo(path='/test1/photo3.jpg', album=album1)
        db.session.add(album1)
        db.session.add(album2)
        db.session.add(photo1)
        db.session.add(photo2)
        db.session.add(photo3)
        db.session.commit()
        self.assertEqual(album1.photos_count,3)
        self.assertEqual(album2.photos_count,0)

        def test_children_count(self):
        album1 = Album(path='/test1')
        album2 = Album(path='/test2')
        child1 = Album(path='/test1/child1', parent=album1)
        child2 = Album(path='/test1/child2', parent=album1)
        child3 = Album(path='/test1/child3', parent=album1)
        db.session.add(album1)
        db.session.add(album2)
        db.session.add(child1)
        db.session.add(child2)
        db.session.add(child3)
        db.session.commit()
        self.assertEqual(album1.children_count,3)
        self.assertEqual(album2.children_count,0)
