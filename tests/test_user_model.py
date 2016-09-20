#coding=utf8

import unittest
from datetime import datetime
from time import sleep
from flask import current_app
from sqlalchemy.exc import IntegrityError
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

    def test_username_uniqueness(self):
        u1 = User(username='test', email='test@test.com')
        u2 = User(username='test', email='test2@test.com')
        with self.assertRaises(IntegrityError):
            db.session.add(u1)
            db.session.add(u2)
            db.session.commit()

    def test_email(self):
        u = User(username='test', email='test@test.com')
        self.assertTrue(u.email == 'test@test.com')

    def test_email_uniqueness(self):
        u1 = User(username='test', email='test@test.com')
        u2 = User(username='test2', email='test@test.com')
        with self.assertRaises(IntegrityError):
            db.session.add(u1)
            db.session.add(u2)
            db.session.commit()

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

    def test_auth_token_expired(self):
        current_app.config['AUTH_TOKEN_EXPIRATION_TIME'] = 1
        u = User(username='test', email='test@test.com')
        db.session.add(u)
        db.session.commit()
        token = u.generate_auth_token()
        sleep(2)
        self.assertFalse(u.verify_auth_token(token))

    def test_get_roles_string(self):
        u = User(username='test', email='test@test.com')
        r1 = Role(name='admin')
        r2 = Role(name='poweruser')
        u.roles.append(r1)
        u.roles.append(r2)
        db.session.add(u)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        roles_string = u.get_roles_string()
        self.assertEqual(roles_string[0],'poweruser')
        self.assertEqual(roles_string[1],'admin')

    def test_registered_at(self):
        u = User(username='test', email='test@test.com')
        db.session.add(u)
        db.session.commit()
        self.assertTrue((datetime.utcnow() - u.registered_at).total_seconds() < 3)

    def test_has_roles(self):
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
