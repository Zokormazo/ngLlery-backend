from flask import current_app
from flask.ext.restful import Resource

class SiteInfo(Resource):
    def get(self):
        value = {
            'name': current_app.config['SITE_NAME'],
            'description': current_app.config['SITE_DESCRIPTION']
        }
        return value
