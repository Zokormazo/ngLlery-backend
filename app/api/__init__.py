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

from .resources.users import UserListResource, UserResource, DashboardUserListResource, DashboardUserResource, DashboardUserRolesResource
api.add_resource(UserListResource, '/user')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(DashboardUserListResource, '/dashboard/user')
api.add_resource(DashboardUserResource, '/dashboard/user/<int:user_id>')
api.add_resource(DashboardUserRolesResource, '/dashboard/user/<int:user_id>/roles/<string:role_name>')

from . import views
