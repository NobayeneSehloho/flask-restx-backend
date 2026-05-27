from flask_restx import fields

from .extensions import api

# --- Course (defined first for nesting in department) ---

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    "department_id": fields.Integer,
    "department_name": fields.String(attribute=lambda c: c.department.name if c.department else None),
})

course_input_model = api.model("CourseInput", {
    "name": fields.String(required=True),
    "department_id": fields.Integer(required=True),
})

course_patch_model = api.model("CoursePatch", {
    "name": fields.String,
    "department_id": fields.Integer,
})

# --- Department ---

department_model = api.model("Department", {
    "id": fields.Integer,
    "name": fields.String,
    "courses": fields.List(fields.Nested(course_model)),
})

department_input_model = api.model("DepartmentInput", {
    "name": fields.String(required=True),
})

department_patch_model = api.model("DepartmentPatch", {
    "name": fields.String,
})

# --- Student ---

student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "student_number": fields.String,
})

student_input_model = api.model("StudentInput", {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "student_number": fields.String(required=True),
})

student_patch_model = api.model("StudentPatch", {
    "name": fields.String,
    "email": fields.String,
    "student_number": fields.String,
})

# --- Teacher ---

teacher_model = api.model("Teacher", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
})

teacher_input_model = api.model("TeacherInput", {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
})

teacher_patch_model = api.model("TeacherPatch", {
    "name": fields.String,
    "email": fields.String,
})

# --- Enrolment (teacher-course) ---

enrolment_model = api.model("Enrolment", {
    "id": fields.Integer,
    "teacher_id": fields.Integer,
    "course_id": fields.Integer,
    "teacher_name": fields.String(attribute=lambda e: e.teacher.name),
    "course_name": fields.String(attribute=lambda e: e.course.name),
    "enrolled_at": fields.DateTime,
    "status": fields.String,
})

enrolment_input_model = api.model("EnrolmentInput", {
    "teacher_id": fields.Integer(required=True),
    "course_id": fields.Integer(required=True),
})

# --- Student Enrolment ---

student_enrolment_model = api.model("StudentEnrolment", {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "course_id": fields.Integer,
    "student_name": fields.String(attribute=lambda e: e.student.name),
    "course_name": fields.String(attribute=lambda e: e.course.name),
    "enrolled_at": fields.DateTime,
    "status": fields.String,
})

student_enrolment_input_model = api.model("StudentEnrolmentInput", {
    "student_id": fields.Integer(required=True),
    "course_id": fields.Integer(required=True),
})
