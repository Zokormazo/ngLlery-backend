#coding=utf-8
import os
from watchdog.events import FileSystemEventHandler
from PIL import Image
from app.models import Album, Photo

class GalleryEventHandler(FileSystemEventHandler):

    def __init__(self,app,db):
        self.app = app
        self.db = db

    def on_created(self,event):
        with self.app.app_context():
            if event.is_directory:
                path = event.src_path
                title = path.split('/')[-1]
                album = Album(path=path,title=title)
                album.parent = Album.query.filter_by(path=os.path.dirname(album.path)).first()
                self.db.session.add(album)
            else:
                try:
                    im = Image.open(event.src_path)
                    photo = Photo(path=event.src_path)
                    parent = Album.query.filter_by(path=os.path.dirname(event.src_path)).first()
                    if parent:
                        parent.photos.append(photo)
                        self.db.session.add(photo)
                        self.db.session.add(parent)
                except IOError:
                    pass
            self.db.session.commit()

    def on_deleted(self,event):
        with self.app.app_context():
            if event.is_directory:
                album = Album.query.filter_by(path=event.src_path).first()
                if album:
                    self.db.session.delete(album)
            else:
                photo = Photo.query.filter_by(path=event.src_path).first()
                if photo:
                    self.db.session.delete(photo)
            self.db.session.commit()

    def on_moved(self,event):
        with self.app.app_context():
            if event.is_directory:
                album = Album.query.filter_by(path=event.src_path).first()
                if album:
                    album.path = event.dest_path
                else:
                    album = Album(path=event.dest_path)
                album.parent = Album.query.filter_by(path=os.path.dirname(event.dest_path)).first()
                self.db.session.add(album)
            else:
                photo = Photo.query.filter_by(path=event.src_path).first()
                parent = Album.query.filter_by(path=os.path.dirname(event.dest_path)).first()
                if photo:
                    if parent:
                        photo.path = event.dest_path
                        parent.photos.append(photo)
                        self.db.session.add(photo)
                        self.db.session.add(parent)
                    else:
                        self.db.session.delete(photo)
            self.db.session.commit()
