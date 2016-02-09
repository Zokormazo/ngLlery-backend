from flask import current_app
from app import db

import hashlib
import hmac
import base64

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)

    # User activity information
    registered_at = db.Column(db.DateTime, default=db.func.now())
    last_seen = db.Column(db.DateTime)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    # Methods
    def verify_password(self, password):
        return self.password == self._hash_password(password)

    def set_password(self, password):
        self.password = self._hash_password(password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['AUTH_SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_roles_string(self):
        return [ role.name for role in self.roles ]

    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.
            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).
            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.
            For example:
                has_roles('a', ('b', 'c'), d)
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        # Translates a list of role objects to a list of role_names
        user_role_names = self.get_roles_string()

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in user_role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in user_role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True

    # Static methods
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['AUTH_SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    # Private methods
    def _hash_password(self, password):
        return base64.b64encode(hmac.new(current_app.config['AUTH_PASSWORD_SALT'], password.encode('utf-8'), hashlib.sha512).digest())

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), nullable=False,unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id =  db.Column(db.Integer(), db.ForeignKey('role.id'))
