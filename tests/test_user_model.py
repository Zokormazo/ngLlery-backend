#coding=utf8

import unittest
import os
from flask import current_app
from app import create_app, db
from app.models import User, Role

class UserModelTestCase(unittest.TestCase):
    '''test user model'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_username(self):
        u = User(username='test', email='test@test.com')
        self.assertTrue(u.username == 'test')

    def test_email(self):
        u = User(username='test', email='test@test.com')
        self.assertTrue(u.email == 'test@test.com')

    def test_password(self):
        u = User(username='test', email='test@test.com')
        u.set_password('test')
        self.assertTrue(u.verify_password('test'))
        self.assertFalse(u.verify_password('foobar'))

    def test_auth_token(self):
        u = User(username='test', email='test@test.com')
        db.session.add(u)
        db.session.commit()
        token = u.generate_auth_token()
        self.assertTrue(u.verify_auth_token(token))
        self.assertFalse(u.verify_auth_token('test'))

    def test_roles(self):
        r1 = Role(name='admin')
        r2 = Role(name='poweruser')
        u1 = User(username='admin', email='admin@test.com')
        u1.roles.append(r1)
        u1.roles.append(r2)
        u2 = User(username='poweruser', email='poweruser@test.com')
        u2.roles.append(r2)
        u3 = User(username='normal', email='normal@test.com')
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        self.assertTrue(u1.has_roles('admin'))
        self.assertTrue(u1.has_roles('poweruser'))
        self.assertTrue(u1.has_roles('admin', 'poweruser'))
        self.assertTrue(u1.has_roles(['admin','poweruser']))
        self.assertFalse(u2.has_roles('admin'))
        self.assertTrue(u2.has_roles('poweruser'))
        self.assertFalse(u2.has_roles('admin', 'poweruser'))
        self.assertTrue(u2.has_roles(['admin', 'poweruser']))
        self.assertFalse(u3.has_roles('admin'))
        self.assertFalse(u3.has_roles('poweruser'))
        self.assertFalse(u3.has_roles('admin', 'poweruser'))
        self.assertFalse(u3.has_roles(['admin', 'poweruser']))
        
