from datetime import datetime, timezone

from .extensions import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    courses = db.relationship("Course", back_populates="department", cascade="all, delete-orphan")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.ForeignKey("department.id"), nullable=False)

    department = db.relationship("Department", back_populates="courses")
    enrolments = db.relationship("Enrolment", back_populates="course", cascade="all, delete-orphan")
    student_enrolments = db.relationship("StudentEnrolment", back_populates="course", cascade="all, delete-orphan")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_number = db.Column(db.String(20), unique=True, nullable=False)

    student_enrolments = db.relationship("StudentEnrolment", back_populates="student", cascade="all, delete-orphan")


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    enrolments = db.relationship("Enrolment", back_populates="teacher", cascade="all, delete-orphan")


class Enrolment(db.Model):
    """Teacher-to-course assignment."""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.ForeignKey("teacher.id"), nullable=False)
    course_id = db.Column(db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default="active", nullable=False)

    teacher = db.relationship("Teacher", back_populates="enrolments")
    course = db.relationship("Course", back_populates="enrolments")

    __table_args__ = (db.UniqueConstraint("teacher_id", "course_id"),)


class StudentEnrolment(db.Model):
    """Student-to-course assignment (many-to-many)."""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default="active", nullable=False)

    student = db.relationship("Student", back_populates="student_enrolments")
    course = db.relationship("Course", back_populates="student_enrolments")

    __table_args__ = (db.UniqueConstraint("student_id", "course_id"),)
