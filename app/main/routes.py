from pathlib import Path

from flask import Blueprint, abort, current_app, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required

from ..models import Announcement


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    announcements = Announcement.query.order_by(Announcement.published_at.desc()).all()
    return render_template("main/dashboard.html", announcements=announcements)


@main_bp.route("/media/announcements/<path:filename>")
@login_required
def announcement_media(filename: str):
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    target = upload_dir / filename
    if not target.exists():
        abort(404)
    return send_from_directory(upload_dir, filename)
