#coding=utf-8

import os
from flask import send_file, current_app, abort
from app.decorators import login_required
from app.models import Photo
from . import blueprint
from PIL import  Image

@blueprint.route('/<int:id>/file')
@login_required
def photo_file(id):
    '''
    Return raw photo file
    '''
    photo = Photo.query.get_or_404(id)
    path = os.path.join(current_app.config['GALLERY_PATH'],photo.path)
    if os.path.exists(path):
        return send_file(path)
    else:
        abort(404)

@blueprint.route('/<int:id>/thumbnail/<int:width>')
@login_required
def photo_thumbnail(id, width):
    '''
    Given an width, return a thumbnail maintaining aspect ratio.
    '''
    photo = Photo.query.get_or_404(id)
    photo_path = os.path.join(current_app.config['GALLERY_PATH'],photo.path)
    cache_dir = os.path.abspath(os.path.join(current_app.config['GALLERY_THUMBNAIL_CACHE'], str(width)))
    thumb_path = os.path.join(cache_dir,str(id))
    if not os.path.exists(thumb_path):
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        im = Image.open(photo_path)
        im.thumbnail((width, 99999999),Image.ANTIALIAS)
        im.save(thumb_path, 'JPEG')
    return send_file(thumb_path)
