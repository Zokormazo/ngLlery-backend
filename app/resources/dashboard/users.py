from flask.ext.restful import Resource, fields, marshal, reqparse, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Role
from app.decorators import roles_required

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'registered_at': fields.DateTime,
    'last_seen': fields.DateTime,
    'roles': fields.List(fields.String(), attribute=lambda x: x.get_roles_string())
}

class DashboardUserList(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')

    def get(self):
        users = User.query.all()
        return {'users': [marshal(user, user_fields) for user in users]}

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        try:
            user = User(username=args['username'],email=args['email'])
            user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            return 204
        except IntegrityError:
            abort(400, message='username or email already exists')

class DashboardUserResource(Resource):
    decorators = [roles_required('admin')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        return {'user': marshal(user, user_fields) }

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        try:
            db.session.delete(user)
            db.session.commit()
            return 204
        except IntegrityError:
            abort(400, message='Can not delete user')

    def put(self, user_id):
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
            return 204
        except IntegrityError:
            abort(400, message='Can not edit user')

class DashboardUserRolesResource(Resource):
    decorators = [roles_required('admin')]

    def put(self, user_id, role_name):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            abort(404, message='Role not found')
        if role in user.roles:
            return 200
        try:
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            return 204
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
            return 200
        try:
            user.roles.remove(role)
            db.session.add(user)
            db.session.commit()
            return 204
        except IntegrityError:
            abort(400, message='Can not delete role from user')
