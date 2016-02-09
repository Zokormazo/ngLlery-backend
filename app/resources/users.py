from flask.ext.restful import Resource, fields, marshal, abort

from app import db
from app.models import User
from app.decorators import login_required

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'registered_at': fields.DateTime,
    'last_seen': fields.DateTime,
    'roles': fields.List(fields.String(), attribute=lambda x: x.get_roles_string())
}

class UserList(Resource):
    decorators = [login_required]

    def get(self):
        users = User.query.all()
        return {'users': [marshal(user, user_fields) for user in users]}

class UserResource(Resource):
    decorators = [login_required]

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return {'user': marshal(user, user_fields) }
