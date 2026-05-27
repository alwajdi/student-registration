from datetime import datetime, timezone

from flask_login import login_user

from ..extensions import db
from ..models import User


def authenticate_user(username: str, password: str) -> User | None:
    user = User.query.filter_by(username=username.strip()).first()
    if user is None or not user.check_password(password) or not user.is_active:
        return None
    return user


def login_authenticated_user(user: User, remember: bool = False) -> None:
    user.last_login_at = datetime.now(timezone.utc)
    login_user(user, remember=remember)
    db.session.commit()
