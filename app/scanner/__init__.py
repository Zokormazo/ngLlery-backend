import os
from watchdog.observers import Observer
from PIL import Image

from app.models import Album, Photo
from . import handler

class Scanner(object):

    def __init__(self, db, app=None, **kwargs):
        self.db = db
        self.app = app

        if app is not None:
            self.init_app(app, **kwargs)

        

    def init_app(self, app):
        self.app = app
        self.app_context = app.app_context()
        
        app.scanner = self
        
        self.event_handler = handler.GalleryEventHandler(self.app,self.db)
        self.observer = Observer()

        self.path = os.path.abspath(app.config['GALLERY_PATH'])
        if app.config['GALLERY_INITIAL_SCAN']:
            self.scan()
        if app.config['GALLERY_WATCHDOG']:
            self.start_observer()

    def start_observer(self):
        if os.path.isdir(self.path):
            self.observer.schedule(self.event_handler, self.path, recursive=True)
            self.observer.start()

    def stop_observer(self):
        self.observer.stop()

    def scan(self):
        with self.app_context:
            for album in Album.query.all():
                if not os.path.isdir(os.path.join(self.path,album.path)):
                    self.db.session.delete(album)
            for photo in Photo.query.all():
                try:
                    im = Image.open(os.path.join(self.path,photo.path))
                except IOError:
                    self.db.session.delete(photo)
            self.db.session.commit()
            if os.path.isdir(self.path):
                self._scan(self.path)

    def _scan(self,path):
        with self.app_context:
            parent = Album.query.filter_by(path=os.path.relpath(path, self.path)).first()
            for file in os.listdir(path):
                file_path = os.path.join(path,file)
                relative_path = os.path.relpath(file_path, self.path)
                if os.path.isdir(file_path):
                    album = Album.query.filter_by(path=relative_path).first()
                    if not album:
                        album = Album(path=relative_path, title=file)
                        self.db.session.add(album)
                        if parent:
                            parent.children.append(album)
                            self.db.session.add(parent)
                        self.db.session.commit()
                    self._scan(file_path)
                elif parent:
                    try:
                        photo = Photo.query.filter_by(path=relative_path).first()
                        im = Image.open(file_path)
                        if not photo:
                            photo = Photo(path=relative_path)
                            parent.photos.append(photo)
                            self.db.session.add(photo)
                            self.db.session.add(parent)
                    except IOError:
                        if photo:
                            self.db.session.delete(photo)
            self.db.session.commit()
