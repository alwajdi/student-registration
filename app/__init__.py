from pathlib import Path

from flask import Flask
from config import Config, INSTANCE_DIR, UPLOAD_DIR
from werkzeug.middleware.proxy_fix import ProxyFix

from .admin.routes import admin_bp
from .auth.routes import auth_bp
from .extensions import csrf, db, login_manager
from .main.routes import main_bp
from .models import User
from .student.routes import student_bp


class PrefixMiddleware:
    def __init__(self, app, prefix: str) -> None:
        self.app = app
        self.prefix = prefix.rstrip("/")

    def __call__(self, environ, start_response):
        forwarded_prefix = environ.get("HTTP_X_FORWARDED_PREFIX", "").rstrip("/")
        script_name = forwarded_prefix or self.prefix
        path_info = environ.get("PATH_INFO", "")

        prefix_matches = path_info == script_name or path_info.startswith(f"{script_name}/")

        if script_name and prefix_matches:
            environ["SCRIPT_NAME"] = script_name
            environ["PATH_INFO"] = path_info[len(script_name):] or "/"
        elif forwarded_prefix:
            environ["SCRIPT_NAME"] = forwarded_prefix

        return self.app(environ, start_response)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1, x_host=1)

    app_root = app.config.get("APPLICATION_ROOT", "").rstrip("/")
    if app_root:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, app_root)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    db_path = INSTANCE_DIR / "app.db"

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    with app.app_context():
        if not db_path.exists() or db_path.stat().st_size == 0:
            db.create_all()
        register_cli(app)

    return app


def register_cli(app: Flask) -> None:
    from .commands import register_commands

    register_commands(app)
