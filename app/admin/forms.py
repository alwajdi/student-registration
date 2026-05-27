from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, DateField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class AnnouncementForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=180)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=4000)])
    image = FileField("Poster image", validators=[FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only.")])
    submit = SubmitField("Publish announcement")


class CourseForm(FlaskForm):
    name = StringField("Course name", validators=[DataRequired(), Length(max=160)])
    course_date = DateField("Course date", validators=[DataRequired()], format="%Y-%m-%d")
    is_available = BooleanField("Available for student enrollment", default=True)
    submit = SubmitField("Save course")


class StudentCreateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    full_name = StringField("Student name", validators=[DataRequired(), Length(max=120)])
    address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    contact_number = StringField("Contact number", validators=[DataRequired(), Length(max=40)])
    submit = SubmitField("Create student account")
