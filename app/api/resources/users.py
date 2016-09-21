#coding=utf8

from flask.ext.restful import Resource, fields, marshal, abort, reqparse
from sqlalchemy.exc import IntegrityError
from flask import g
from app import db
from app.models import User, Role
from app.decorators import login_required, roles_required
from app.api.types import email

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'registered_at': fields.DateTime,
    'last_seen': fields.DateTime,
    'roles': fields.List(fields.String(), attribute=lambda x: x.get_roles_string())
}

dash_user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'registered_at': fields.DateTime,
    'last_seen': fields.DateTime,
    'roles': fields.List(fields.String(), attribute=lambda x: x.get_roles_string())
}

class UserListResource(Resource):
    decorators = [login_required]

    def get(self):
        users = User.query.all()
        return [marshal(user, user_fields) for user in users]

class UserResource(Resource):
    decorators = [login_required]

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return marshal(user, user_fields)

class ProfileResource(Resource):
    decorators = [login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=email, location='json')
        self.reqparse.add_argument('password', location='json')
        super(ProfileResource, self).__init__()

    def get(self):
        return marshal(g.user, dash_user_fields)

    def post(self):
        args = self.reqparse.parse_args()
        try:
            if args['email']:
                g.user.email = args['email']
            if args['password']:
                g.user.set_password(args['password'])
            db.session.add(g.user)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not edit user')

class DashboardUserListResource(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='No username provided', location='json')
        self.reqparse.add_argument('password', required=True, help='No password provided', location='json')
        self.reqparse.add_argument('email', type=email, required=True, help='No email provided', location='json')
        super(DashboardUserListResource, self).__init__()

    def get(self):
        users = User.query.all()
        return [marshal(user, dash_user_fields) for user in users]

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        try:
            user = User(username=args['username'],email=args['email'])
            user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            return marshal(user, dash_user_fields)
        except IntegrityError:
            abort(400, message='username or email already exists')

class DashboardUserResource(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', location='json')
        self.reqparse.add_argument('email', type=email, location='json')
        self.reqparse.add_argument('password', location='json')
        super(DashboardUserResource, self).__init__()

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        return marshal(user, dash_user_fields)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        try:
            db.session.delete(user)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not delete user')

    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        args = self.reqparse.parse_args()
        try:
            if args['username']:
                user.username = args['username']
            if args['email']:
                user.email = args['email']
            if args['password']:
                user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not edit user')

class DashboardUserRolesResource(Resource):
    decorators = [roles_required('admin')]

    def post(self, user_id, role_name):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            abort(404, message='Role not found')
        if role in user.roles:
            return None,204
        try:
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not add role to user')

    def delete(self, user_id, role_name):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        role =  Role.query.filter_by(name=role_name).first()
        if not role:
            abort(404, message='Role not found')
        if not role in user.roles:
            return None,204
        try:
            user.roles.remove(role)
            db.session.add(user)
            db.session.commit()
            return None,204
        except IntegrityError:
            abort(400, message='Can not delete role from user')
