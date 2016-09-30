#coding=utf-8
import os
from watchdog.events import FileSystemEventHandler
from PIL import Image
from app.models import Album, Photo

class GalleryEventHandler(FileSystemEventHandler):

    def __init__(self,app,db):
        self.app = app
        self.db = db
        with self.app.app_context():
            self.path = os.path.abspath(self.app.config['GALLERY_PATH'])

    def on_created(self,event):
        with self.app.app_context():
            path = os.path.relpath(event.src_path,self.path)
            if event.is_directory:
                album = Album(path=path, title=os.path.basename(event.src_path))
                album.parent = Album.query.filter_by(path=os.path.dirname(path)).first()
                self.db.session.add(album)
            else:
                try:
                    im = Image.open(os.path.join(self.path,path))
                    photo = Photo(path=path)
                    parent = Album.query.filter_by(path=os.path.dirname(path)).first()
                    if parent:
                        parent.photos.append(photo)
                        self.db.session.add(photo)
                        self.db.session.add(parent)
                except IOError:
                    pass
            self.db.session.commit()

    def on_deleted(self,event):
        with self.app.app_context():
            path = os.path.relpath(event.src_path,self.path)
            if event.is_directory:
                album = Album.query.filter_by(path=path).one()
                if album:
                    self.db.session.delete(album)
            else:
                photo = Photo.query.filter_by(path=path).one()
                if photo:
                    self.db.session.delete(photo)
            self.db.session.commit()

    def on_moved(self,event):
        with self.app.app_context():
            src_path = os.path.relpath(event.src_path,self.path)
            dest_path = os.path.relpath(event.dest_path,self.path)
            if event.is_directory:
                album = Album.query.filter_by(path=src_path).first()
                if album:
                    album.path = dest_path
                else:
                    album = Album(path=dest_path)
                album.parent = Album.query.filter_by(path=os.path.dirname(dest_path)).first()
                self.db.session.add(album)
            else:
                photo = Photo.query.filter_by(path=src_path).first()
                parent = Album.query.filter_by(path=os.path.dirname(dest_path)).first()
                if photo:
                    if parent:
                        photo.path = dest_path
                        parent.photos.append(photo)
                        self.db.session.add(photo)
                        self.db.session.add(parent)
                    else:
                        self.db.session.delete(photo)
            self.db.session.commit()
