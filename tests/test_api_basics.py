#coding=utf8

import unittest
from app import create_app
from app.api import api
from app.api.types import email, rfc822

class ApiBasicsTestCase(unittest.TestCase):
    '''Test Api Basics'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_headers(self, token=''):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
    
    def test_api_404(self):
        response = self.client.get('/wrong-url', headers=self.get_headers())
        self.assertTrue(response.status_code == 404)

    def test_email(self):
        self.assertTrue(email('test@test.com'))
        with self.assertRaises(ValueError):
            email('not an email')

    def test_rfc822(self):
        self.assertTrue(rfc822('Wed, 02 Oct 2002 13:00:00 GMT'))
        with self.assertRaises(ValueError):
            rfc822('invalid datetime')
