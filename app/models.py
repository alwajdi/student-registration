from __future__ import annotations

from datetime import date, datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active_user = db.Column("is_active", db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    student_profile = db.relationship("Student", back_populates="user", uselist=False)
    created_courses = db.relationship("Course", back_populates="created_by", foreign_keys="Course.created_by_user_id")
    created_announcements = db.relationship(
        "Announcement", back_populates="created_by", foreign_keys="Announcement.created_by_user_id"
    )
    reviewed_enrollments = db.relationship(
        "Enrollment", back_populates="reviewed_by", foreign_keys="Enrollment.reviewed_by_user_id"
    )

    @property
    def is_active(self) -> bool:
        return self.is_active_user

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_student(self) -> bool:
        return self.role == "student"


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact_number = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    course_date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    created_by = db.relationship("User", back_populates="created_courses", foreign_keys=[created_by_user_id])
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    @property
    def is_open_for_students(self) -> bool:
        return self.is_available and self.course_date >= date.today()


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),)

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)
    requested_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    reviewed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    reviewed_by = db.relationship("User", back_populates="reviewed_enrollments", foreign_keys=[reviewed_by_user_id])


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    published_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    created_by = db.relationship("User", back_populates="created_announcements", foreign_keys=[created_by_user_id])
