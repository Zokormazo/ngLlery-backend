#coding=utf8

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api

from config import config

# Create db object
db = SQLAlchemy()
# Create Scanner object
from app.scanner import Scanner
scanner = Scanner(db)
#create api object
api = None

def create_app(config_name):
    # Setup Flask app and load config.py
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize module objects

    db.init_app(app)
    scanner.init_app(app)

    from app.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.images import blueprint as images_blueprint
    app.register_blueprint(images_blueprint, url_prefix='/images')

    return app
