#coding=utf8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

#create db object
db = SQLAlchemy()

def create_app(config_name):
    # Setup Flask app and load config.py
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    return app
