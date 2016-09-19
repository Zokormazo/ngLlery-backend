#coding=utf8

import unittest
from app import create_app
from app.api import api

class Api404TestCase(unittest.TestCase):
    '''test api'''
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
        
                           
