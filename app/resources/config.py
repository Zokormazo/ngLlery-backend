from flask import current_app
from flask.ext.restful import Resource, fields, marshal

siteinfo_fields = {
    'name' : fields.String,
    'description' : fields.String
}

auth_fields = {
    'tokenExpirationTime': fields.Integer,
    'enableRegistration': fields.Boolean
}

info_fields = {
    'info': fields.Nested(siteinfo_fields),
    'auth': fields.Nested(auth_fields)
}

class ConfigResource(Resource):
    def get(self):
        value = {
            'info': {
                'name': current_app.config['SITE_NAME'],
                'description': current_app.config['SITE_DESCRIPTION']
            },
            'auth': {
                'tokenExpirationTime': current_app.config['AUTH_TOKEN_EXPIRATION_TIME'],
                'enableRegistration': current_app.config['AUTH_ENABLE_REGISTRATION']
            }
        }
        return { 'config': marshal(value,info_fields) }
