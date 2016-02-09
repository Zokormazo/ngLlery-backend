from flask.ext.restful import Resource, fields, marshal

from app import db
from app.models import User
from app.decorators import login_required

class AlbumList(Resource):
    decorators = [login_required]

    def get(self):
        albums = [
            {'name': 'Album1'},
            {'name': 'Album2'},
            {'name': 'Album3'}  
        ]
        return { 'albums': albums }
