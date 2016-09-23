#coding=utf-8

import unittest
import os
import shutil
from time import sleep
from flask import current_app
from app import create_app, db
from app.models import Album, Photo
from PIL import Image

TESTING_DIR = 'testing_dir'
TEST_PHOTO_FILE = TESTING_DIR + '/test.jpg'
TEST_NON_PHOTO_FILE = TESTING_DIR + '/test.nophoto'

class ScannerTestCase(unittest.TestCase):
    '''Test Scanner'''

    @classmethod
    def setUpClass(self):
        os.makedirs(TESTING_DIR)
        im = Image.new('RGB', (3648,2736))
        im.save(TEST_PHOTO_FILE, 'JPEG')
        open(TEST_NON_PHOTO_FILE, 'a').close()

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(TESTING_DIR)
        pass

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.assertFalse(os.path.exists(current_app.config['GALLERY_PATH']));
        os.makedirs(current_app.config['GALLERY_PATH'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        shutil.rmtree(current_app.config['GALLERY_PATH'])
        self.app_context.pop()

    def test_scan(self):
        path = current_app.config['GALLERY_PATH']
        '''
            Test 1: empty directory
        '''
        self.app.scanner.scan()
        self.assertEqual(Album.query.count(),0)
        self.assertEqual(Photo.query.count(),0)
        '''
            Test 2:

            album1/ [d]
                album2/ [d]
                    album3/ [d]
                    photo1.jpg [f:JPEG]
                    photo2.jpg [f:JPEG]
                    photo3.jpg [f:JPEG]
                photo1.jpg [f:JPEG]
                photo2.jpg [f:JPEG]
                photo3.jpg [f:JPEG]
                photo4.jpg [f:JPEG]
                non_photo.jpg [f:None]
            album4/ [d]
                photo1.jpg [f:JPEG]
                photo2.jpg [f:JPEG]
            photo1.jpg [f:JPEG]
        '''
        os.makedirs(os.path.join(path,'album1/album2/album3'))
        os.makedirs(os.path.join(path,'album4'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/photo1.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/photo2.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/photo3.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/photo4.jpg'))
        shutil.copy(TEST_NON_PHOTO_FILE,os.path.join(path,'album1/non_photo.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/album2/photo1.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/album2/photo2.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album1/album2/photo3.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album4/photo1.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'album4/photo2.jpg'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,'photo1.jpg'))
        self.app.scanner.scan()
        self.assertEqual(Album.query.count(),4)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1')).first().children),1)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().children),1)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2/album3')).first().children),0)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album4')).first().children),0)
        self.assertEqual(Photo.query.count(),9)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1')).first().photos.count(),4)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().photos.count(),3)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2/album3')).first().photos.count(),0)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album4')).first().photos.count(),2)
        '''
            Test 3:

            album1/ [d]
                album2/ [d]
                    photo1.jpg [f:JPEG]
                    photo2.jpg [f:None]
                    photo3.jpg [f:JPEG]
                photo1.jpg/ [d]
                    photo1.jpg [f:JPEG]
                photo2.jpg [f:JPEG]
            album3/ [d]
                photo1.jpg [f:JPEG]
                photo2.jpg [f:JPEG]
            album4 [f:JPEG]
            photo1.jpg [f:JPEG]
            
        '''
        shutil.rmtree(os.path.join(path, 'album1/album2/album3'))
        shutil.copy(TEST_NON_PHOTO_FILE,os.path.join(path,'album1/album2/photo2.jpg'))
        os.remove(os.path.join(path,'album1/photo1.jpg'))
        os.mkdir(os.path.join(path,'album1/photo1.jpg'))
        shutil.copy(TEST_PHOTO_FILE, os.path.join(path,'album1/photo1.jpg/photo1.jpg'))
        os.remove(os.path.join(path, 'album1/photo3.jpg'))
        os.remove(os.path.join(path, 'album1/photo4.jpg'))
        os.rename(os.path.join(path,'album4'),os.path.join(path,'album3'))
        shutil.copy(TEST_PHOTO_FILE, os.path.join(path, 'album4'))
        self.app.scanner.scan()
        self.assertEqual(Album.query.count(),4)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1')).first().children),2)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().children),0)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/photo1.jpg')).first().children),0)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album3')).first().children),0)
        self.assertEqual(Photo.query.count(),6)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1')).first().photos.count(),1)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().photos.count(),2)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/photo1.jpg')).first().photos.count(),1)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album3')).first().photos.count(),2)
        '''
            Test 4: empty directory
        '''
        shutil.rmtree(path)
        os.mkdir(path)
        self.app.scanner.scan()
        self.assertEqual(Album.query.count(),0)
        self.assertEqual(Photo.query.count(),0)

    def test_observer(self):
        path = current_app.config['GALLERY_PATH']
        self.app.scanner.start_observer()
        os.makedirs(os.path.join(path,'album1/album2/album3'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path,  'album1/photo1.jpg'))
        shutil.copy(TEST_NON_PHOTO_FILE,os.path.join(path,'album1/album2/photo1.jpg'))
        sleep(1)
        self.assertEqual(Album.query.count(),3)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1')).first().children),1)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().children),1)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2/album3')).first().children),0)
        self.assertEqual(Photo.query.count(),1)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1')).first().photos.count(),1)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().photos.count(),0)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2/album3')).first().photos.count(),0)
        os.makedirs(os.path.join(path,'album4'))
        shutil.copy(TEST_PHOTO_FILE,os.path.join(path, 'album4/photo1.jpg'))
        shutil.rmtree(os.path.join(path,'album1/album2/album3'))
        sleep(1)
        self.assertEqual(Album.query.count(),3)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1')).first().children),1)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().children),0)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album4')).first().children),0)
        self.assertEqual(Photo.query.count(),2)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1')).first().photos.count(),1)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album1/album2')).first().photos.count(),0)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album4')).first().photos.count(),1)
        os.rename(os.path.join(path,'album1/photo1.jpg'),os.path.join(path,'album4/photo2.jpg'))
        os.rename(os.path.join(path,'album1/album2'),os.path.join(path,'album4/album2'))
        shutil.rmtree(os.path.join(path,'album1'))
        sleep(1)
        self.assertEqual(Album.query.count(),2)
        self.assertEqual(len(Album.query.filter_by(path=os.path.join(path, 'album4')).first().children),1)
        self.assertEqual(Photo.query.count(),2)
        self.assertEqual(Album.query.filter_by(path=os.path.join(path, 'album4')).first().photos.count(),2)
        os.rename(os.path.join(path,'album4/photo1.jpg'),os.path.join(path,'photo1.jpg'))
        os.rename(os.path.join(path,'album4/photo2.jpg'),os.path.join(path,'photo2.jpg'))
        sleep(1)
        self.assertEqual(Photo.query.count(),0)
        self.app.scanner.stop_observer()
        
