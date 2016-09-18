#coding=utf8

from flask import current_app, g
from flask.ext.restful import Resource, reqparse, fields, marshal, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User
from app.decorators import login_required

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'roles': fields.List(fields.String(), attribute=lambda x: x.get_roles_string())
}

class LoginResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(LoginResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        user = User.query.filter_by(username=args['username']).first()
        if user and user.verify_password(args['password']):
            userValue = marshal(user, user_fields)
            token = user.generate_auth_token()
            value = {
                'user': userValue,
                'token': token
            }
            return value
        else:
            abort(400, message='Invalid username/password')

class RegisterResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        super(RegisterResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        if not current_app.config['AUTH_ENABLE_REGISTRATION']:
            abort(400, message='user registration disabled')
        try:
            user = User(username=args['username'],email=args['email'])
            user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            return 201
        except IntegrityError:
            abort(400, message='username or email already exists')

class TokenResource(Resource):
    decorators = [login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return { 'user': marshal(g.user, user_fields), 'token': token }
