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

    api = Api(app,prefix='/api')

    from app.resources.config import ConfigResource
    api.add_resource(ConfigResource, '/config')

    from app.resources.auth import Login, Register
    api.add_resource(Login, '/login')
    api.add_resource(Register, '/register')

    from app.resources.users import UserList, UserResource
    api.add_resource(UserList, '/users')
    api.add_resource(UserResource, '/user/<int:user_id>')

    from app.resources.dashboard.users import DashboardUserList, DashboardUserResource, DashboardUserRolesResource
    api.add_resource(DashboardUserList, '/dashboard/users')
    api.add_resource(DashboardUserResource, '/dashboard/user/<int:user_id>')
    api.add_resource(DashboardUserRolesResource, '/dashboard/user/<int:user_id>/roles/<string:role_name>')

    from app.requests import blueprint as requests_blueprint
    app.register_blueprint(requests_blueprint)

    return app
