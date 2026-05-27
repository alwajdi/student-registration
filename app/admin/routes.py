from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..decorators import role_required
from ..extensions import db
from ..models import Announcement, Course, Enrollment, Student, User
from ..services.announcement_service import create_announcement, save_announcement_image
from ..services.course_service import create_course
from ..services.enrollment_service import review_enrollment
from .forms import AnnouncementForm, CourseForm, StudentCreateForm


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/announcements")
@login_required
@role_required("admin")
def announcements():
    items = Announcement.query.order_by(Announcement.published_at.desc()).all()
    return render_template("admin/announcements.html", announcements=items)


@admin_bp.route("/announcements/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def announcement_create():
    from flask_login import current_user

    form = AnnouncementForm()
    if form.validate_on_submit():
        try:
            image_name = save_announcement_image(form.image.data)
            create_announcement(form.title.data, form.content.data, current_user, image_name)
            flash("Announcement published.", "success")
            return redirect(url_for("admin.announcements"))
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template("admin/announcement_form.html", form=form)


@admin_bp.route("/courses")
@login_required
@role_required("admin")
def courses():
    items = Course.query.order_by(Course.course_date.asc(), Course.name.asc()).all()
    return render_template("admin/courses.html", courses=items)


@admin_bp.route("/courses/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def course_create():
    from flask_login import current_user

    form = CourseForm()
    if form.validate_on_submit():
        create_course(form.name.data, form.course_date.data, bool(form.is_available.data), current_user)
        flash("Course saved.", "success")
        return redirect(url_for("admin.courses"))

    return render_template("admin/course_form.html", form=form)


@admin_bp.route("/courses/<int:course_id>")
@login_required
@role_required("admin")
def course_detail(course_id: int):
    course = Course.query.get_or_404(course_id)
    enrollments = (
        Enrollment.query.filter_by(course_id=course.id)
        .join(Student)
        .order_by(Enrollment.status.asc(), Student.full_name.asc())
        .all()
    )
    return render_template("admin/course_detail.html", course=course, enrollments=enrollments)


@admin_bp.route("/enrollments")
@login_required
@role_required("admin")
def enrollments():
    status = request.args.get("status", "pending")
    query = Enrollment.query.join(Student).join(Course)
    if status in {"pending", "approved", "rejected"}:
        query = query.filter(Enrollment.status == status)
    items = query.order_by(Enrollment.requested_at.desc()).all()
    return render_template("admin/enrollments.html", enrollments=items, current_status=status)


@admin_bp.route("/enrollments/<int:enrollment_id>/review", methods=["POST"])
@login_required
@role_required("admin")
def enrollment_review(enrollment_id: int):
    from flask_login import current_user

    enrollment = Enrollment.query.get_or_404(enrollment_id)
    decision = request.form.get("decision", "").strip().lower()
    try:
        review_enrollment(enrollment, current_user, decision)
        flash(f"Enrollment {decision}.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin.enrollments", status="pending"))


@admin_bp.route("/students")
@login_required
@role_required("admin")
def students():
    items = Student.query.order_by(Student.full_name.asc()).all()
    return render_template("admin/students.html", students=items)


@admin_bp.route("/students/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def student_create():
    form = StudentCreateForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.strip()).first():
            flash("That username is already in use.", "error")
            return render_template("admin/student_form.html", form=form)
        if Student.query.filter_by(email=form.email.data.strip().lower()).first():
            flash("That email address is already in use.", "error")
            return render_template("admin/student_form.html", form=form)

        user = User(username=form.username.data.strip(), role="student")
        user.set_password(form.password.data)
        student = Student(
            user=user,
            full_name=form.full_name.data.strip(),
            address=form.address.data.strip(),
            email=form.email.data.strip().lower(),
            contact_number=form.contact_number.data.strip(),
        )
        db.session.add_all([user, student])
        db.session.commit()
        flash("Student account created.", "success")
        return redirect(url_for("admin.students"))

    return render_template("admin/student_form.html", form=form)
