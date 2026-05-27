from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(role: str):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.role != role:
                return abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
