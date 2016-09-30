#coding=utf8

import os;
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SITE_NAME = 'Argazkiak'
    SITE_DESCRIPTION = 'Gure familitxoko argazki bilduma'

    AUTH_ENABLE_REGISTRATION = True
    AUTH_TOKEN_EXPIRATION_TIME = 600
    AUTH_SECRET_KEY = 'My Secret Key'
    AUTH_PASSWORD_SALT = 'AAAA'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GALLERY_PATH = 'gallery/'
    GALLERY_WATCHDOG = True
    GALLERY_INITIAL_SCAN = True
    GALLERY_THUMBNAIL_CACHING = True
    GALLERY_THUMBNAIL_CACHE = 'cache/'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db/data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db/data-test.sqlite')

    GALLERY_PATH = 'testing_dir/gallery'
    GALLERY_INITIAL_SCAN = False
    GALLERY_WATCHDOG = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db/data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
