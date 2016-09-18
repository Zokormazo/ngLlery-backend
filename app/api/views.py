#coding=utf8
from datetime import datetime;
from flask import request
from app import db
from app.models import User
from . import blueprint

@blueprint.after_app_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@blueprint.before_app_request
def before_request():
    token = request.headers.get('Authorization')
    if token:
        user = User.verify_auth_token(token)
        if user:
            user.last_seen = datetime.utcnow()
            db.session.add(user)
            db.session.commit()

