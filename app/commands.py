from datetime import date

import click
from flask import Flask

from .extensions import db
from .models import Announcement, Course, Student, User


def register_commands(app: Flask) -> None:
    @app.cli.command("seed")
    def seed() -> None:
        """Seed the database with demo data."""
        if User.query.filter_by(username="admin").first():
            click.echo("Seed data already exists.")
            return

        admin = User(username="admin", role="admin")
        admin.set_password("admin123!")
        db.session.add(admin)
        db.session.flush()

        student_user = User(username="student1", role="student")
        student_user.set_password("student123!")
        db.session.add(student_user)
        db.session.flush()

        student = Student(
            user=student_user,
            full_name="Ariana Mateo",
            address="42 Academy Avenue",
            email="ariana.mateo@example.edu",
            contact_number="+1-555-0100",
        )
        db.session.add(student)

        course = Course(
            name="Professional Communication for Analysts",
            course_date=date.fromisoformat("2026-06-15"),
            is_available=True,
            created_by=admin,
        )
        db.session.add(course)

        announcement = Announcement(
            title="Admissions Orientation Week",
            content="Orientation sessions are now open. Please review the schedule and arrive 15 minutes early.",
            created_by=admin,
        )
        db.session.add(announcement)

        db.session.commit()
        click.echo("Seed complete. Admin: admin / admin123!  Student: student1 / student123!")
