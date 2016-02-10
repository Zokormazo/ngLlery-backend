#coding=utf8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api

from config import config

# Create db object
db = SQLAlchemy()
#create api object
api = None

def create_app(config_name):
    # Setup Flask app and load config.py
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize module objects

    db.init_app(app)

    from app.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
