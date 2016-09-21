# coding=utf8

from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

from .resources.config import ConfigResource
api.add_resource(ConfigResource, '/config')

from .resources.auth import LoginResource, RegisterResource, TokenResource
api.add_resource(LoginResource, '/login')
api.add_resource(RegisterResource, '/register')
api.add_resource(TokenResource, '/token')

from .resources.users import UserListResource, UserResource, DashboardUserListResource, DashboardUserResource, DashboardUserRolesResource, ProfileResource
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(DashboardUserListResource, '/dashboard/users')
api.add_resource(DashboardUserResource, '/dashboard/users/<int:user_id>')
api.add_resource(DashboardUserRolesResource, '/dashboard/users/<int:user_id>/roles/<string:role_name>')
api.add_resource(ProfileResource, '/profile')

from . import views
