from pathlib import Path

from flask import Flask

from config import Config, INSTANCE_DIR, UPLOAD_DIR

from .admin.routes import admin_bp
from .auth.routes import auth_bp
from .extensions import csrf, db, login_manager
from .main.routes import main_bp
from .models import User
from .student.routes import student_bp

from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1, x_host=1)
    
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
