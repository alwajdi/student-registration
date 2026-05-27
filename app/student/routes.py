from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..decorators import role_required
from ..models import Course, Enrollment
from ..services.enrollment_service import request_enrollment


student_bp = Blueprint("student", __name__, url_prefix="/student")


def _current_student():
    return current_user.student_profile


@student_bp.route("/courses")
@login_required
@role_required("student")
def available_courses():
    courses = Course.query.order_by(Course.course_date.asc(), Course.name.asc()).all()
    enrollments = {
        enrollment.course_id: enrollment.status
        for enrollment in Enrollment.query.filter_by(student_id=_current_student().id).all()
    }
    visible_courses = [course for course in courses if course.is_open_for_students]
    return render_template("student/courses.html", courses=visible_courses, enrollment_map=enrollments)


@student_bp.route("/courses/<int:course_id>/enroll", methods=["POST"])
@login_required
@role_required("student")
def enroll(course_id: int):
    course = Course.query.get_or_404(course_id)
    try:
        request_enrollment(_current_student(), course)
        flash("Enrollment request submitted for review.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("student.available_courses"))


@student_bp.route("/enrollments")
@login_required
@role_required("student")
def my_enrollments():
    enrollments = (
        Enrollment.query.filter_by(student_id=_current_student().id)
        .join(Course)
        .order_by(Course.course_date.asc(), Course.name.asc())
        .all()
    )
    return render_template("student/enrollments.html", enrollments=enrollments)


@student_bp.route("/courses/<int:course_id>")
@login_required
@role_required("student")
def course_detail(course_id: int):
    enrollment = (
        Enrollment.query.filter_by(student_id=_current_student().id, course_id=course_id, status="approved").first_or_404()
    )
    classmates = (
        Enrollment.query.filter_by(course_id=course_id, status="approved")
        .filter(Enrollment.student_id != _current_student().id)
        .all()
    )
    return render_template("student/course_detail.html", enrollment=enrollment, classmates=classmates)


@student_bp.route("/profile")
@login_required
@role_required("student")
def profile():
    return render_template("student/profile.html", student=_current_student())
