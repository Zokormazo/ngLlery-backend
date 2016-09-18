from functools import wraps
from flask import request, abort, g

from app.models import User

def login_required(f):
    """ This decorator ensures that the current user is logged in before calling the actual view.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method != 'OPTIONS':
            token = request.headers.get('Authorization')
            if not token:
                abort(401)
            user = User.verify_auth_token(token)
            if not user:
                abort(401)
            g.user = user
        return f(*args, **kwargs)        
    return decorated

def roles_required(*role_names):
    """ This decorator ensures that the current user has all of the specified roles.
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method != 'OPTIONS':
                token = request.headers.get('Authorization')
                if not token:
                    abort(401)
                user = User.verify_auth_token(token)
                if not user:
                    abort(401)
                g.user = user

                # User must have the required roles
                if not user.has_roles(*role_names):
                    # Redirect to the unauthorized page
                    abort(403)

            # Call the actual view
            return func(*args, **kwargs)
        return decorated_view
    return wrapper
