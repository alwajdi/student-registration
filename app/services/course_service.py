from ..extensions import db
from ..models import Course, User


def create_course(name: str, course_date, is_available: bool, created_by: User) -> Course:
    course = Course(
        name=name.strip(),
        course_date=course_date,
        is_available=is_available,
        created_by=created_by,
    )
    db.session.add(course)
    db.session.commit()
    return course
