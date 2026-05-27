from datetime import datetime, timezone

from ..extensions import db
from ..models import Course, Enrollment, Student, User


def request_enrollment(student: Student, course: Course) -> Enrollment:
    existing = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
    if existing:
        raise ValueError("You already have an enrollment request for this course.")

    if not course.is_open_for_students:
        raise ValueError("This course is not currently available for enrollment.")

    enrollment = Enrollment(student=student, course=course, status="pending")
    db.session.add(enrollment)
    db.session.commit()
    return enrollment


def review_enrollment(enrollment: Enrollment, reviewer: User, status: str) -> Enrollment:
    if status not in {"approved", "rejected"}:
        raise ValueError("Invalid enrollment status.")

    enrollment.status = status
    enrollment.reviewed_by = reviewer
    enrollment.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()
    return enrollment
