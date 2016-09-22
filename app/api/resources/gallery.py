#coding=utf8

from flask.ext.restful import Resource, reqparse, fields, marshal, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Album, Photo
from app.decorators import login_required, roles_required
from app.api.types import rfc822

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'timestamp_from': fields.DateTime,
    'timestamp_to': fields.DateTime
}

dash_album_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'title': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'timestamp_from': fields.DateTime,
    'timestamp_to': fields.DateTime
}

photo_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'timestamp': fields.DateTime
}

dash_photo_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'title': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'timestamp': fields.DateTime
}

class AlbumListResource(Resource):
    decorators = [login_required]

    def get(self):
        albums = Album.query.filter_by(parent=None)
        return [marshal(album, album_fields) for album in albums]

class AlbumResource(Resource):
    decorators = [login_required]

    def get(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        return marshal(album, album_fields)

class AlbumChildrenListResource(Resource):
    decorators = [login_required]

    def get(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        children = Album.query.filter_by(parent=album)
        return [marshal(child, album_fields) for child in children]

class AlbumPhotosListResource(Resource):
    decorators = [login_required]
    
    def get(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        photos = Photo.query.filter_by(album=album)
        return [marshal(photo, photo_fields) for photo in photos]

class PhotoResource(Resource):
    decorators = [login_required]
    
    def get(self, photo_id):
        photo = Photo.query.get(photo_id)
        if not photo:
            abort(404, message="Photo not found")
        return marshal(photo, photo_fields)

class DashboardAlbumListResource(Resource):
    decorators = [roles_required('admin')]
    
    def get(self):
        albums = Album.query.filter_by(parent=None)
        return [marshal(album, dash_album_fields) for album in albums]

class DashboardAlbumResource(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=unicode, location='json')
        self.reqparse.add_argument('description', type=unicode, location='json')
        self.reqparse.add_argument('timestamp_from', type=rfc822, location='json')
        self.reqparse.add_argument('timestamp_to', type=rfc822, location='json')
        super(DashboardAlbumResource, self).__init__()

    def get(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        return marshal(album, dash_album_fields)

    def post(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        args = self.reqparse.parse_args()
        try:
            if args['title']:
                album.title = args['title']
            if args['description']:
                album.description = args['description']
            if args['timestamp_from']:
                album.timestamp_from = args['timestamp_from']
            if args['timestamp_to']:
                album.timestamp_to = args['timestamp_to']
            db.session.add(album)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not edit album')

class DashboardAlbumChildrenListResource(Resource):
    decorators = [roles_required('admin')]

    def get(self,album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        children = Album.query.filter_by(parent=album)
        return [marshal(child, dash_album_fields) for child in children]
    

class DashboardAlbumPhotosListResource(Resource):
    decorators = [roles_required('admin')]

    def get(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")
        photos = Photo.query.filter_by(album=album)
        return [marshal(photo, dash_photo_fields) for photo in photos]

class DashboardPhotoResource(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=unicode, location='json')
        self.reqparse.add_argument('description', type=unicode, location='json')
        self.reqparse.add_argument('timestamp', type=rfc822, location='json')
        super(DashboardPhotoResource, self).__init__()

    def get(self, photo_id):
        photo = Photo.query.get(photo_id)
        if not photo:
            abort(404, message="Photo not found")
        return marshal(photo, dash_photo_fields)

    def post(self, photo_id):
        photo = Photo.query.get(photo_id)
        if not photo:
            abort(404, message="Photo not found")
        args = self.reqparse.parse_args()
        try:
            if args['title']:
                photo.title = args['title']
            if args['description']:
                photo.description = args['description']
            if args['timestamp']:
                photo.timestamp_from = args['timestamp']
            db.session.add(photo)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not edit photo')
