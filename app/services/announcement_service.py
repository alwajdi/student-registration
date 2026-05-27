from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Announcement, User


def save_announcement_image(upload: FileStorage | None) -> str | None:
    if upload is None or not upload.filename:
        return None

    filename = secure_filename(upload.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    allowed = current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
    if extension not in allowed:
        raise ValueError("Unsupported image type.")

    unique_name = f"{uuid4().hex}.{extension}"
    destination = Path(current_app.config["UPLOAD_FOLDER"]) / unique_name
    upload.save(destination)
    return unique_name


def create_announcement(title: str, content: str, created_by: User, image_name: str | None) -> Announcement:
    announcement = Announcement(
        title=title.strip(),
        content=content.strip(),
        image_path=image_name,
        created_by=created_by,
    )
    db.session.add(announcement)
    db.session.commit()
    return announcement
