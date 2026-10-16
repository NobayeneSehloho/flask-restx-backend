from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError

from .api_models import (
    course_model, course_input_model, course_patch_model,
    student_model, student_input_model, student_patch_model,
    teacher_model, teacher_input_model, teacher_patch_model,
    enrolment_model, enrolment_input_model,
    department_model, department_input_model, department_patch_model,
    student_enrolment_model, student_enrolment_input_model,
)
from .extensions import db
from .models import Course, Student, Teacher, Enrolment, Department, StudentEnrolment
from .security import token_required

ns = Namespace("api")


@ns.route("/hello")
class Hello(Resource):
    method_decorators = [token_required]

    def get(self):
        return {"hello": "restx"}


# --- Departments ---

@ns.route("/departments")
class DepartmentListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(department_model)
    def get(self):
        return Department.query.all()

    @ns.expect(department_input_model)
    @ns.marshal_with(department_model, code=201)
    def post(self):
        dept = Department(name=ns.payload["name"])
        db.session.add(dept)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Department name already exists")
        return dept, 201


@ns.route("/departments/<int:id>")
class DepartmentAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(department_model)
    def get(self, id):
        return Department.query.get_or_404(id, description="Department not found")

    @ns.expect(department_input_model)
    @ns.marshal_with(department_model)
    def put(self, id):
        dept = Department.query.get_or_404(id, description="Department not found")
        dept.name = ns.payload["name"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Department name already exists")
        return dept

    @ns.expect(department_patch_model)
    @ns.marshal_with(department_model)
    def patch(self, id):
        dept = Department.query.get_or_404(id, description="Department not found")
        if "name" in ns.payload:
            dept.name = ns.payload["name"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Department name already exists")
        return dept

    def delete(self, id):
        dept = Department.query.get_or_404(id, description="Department not found")
        db.session.delete(dept)
        db.session.commit()
        return {}, 204


@ns.route("/departments/<int:id>/courses")
class DepartmentCoursesAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(course_model)
    def get(self, id):
        dept = Department.query.get_or_404(id, description="Department not found")
        return dept.courses


# --- Courses ---

@ns.route("/courses")
class CourseListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model, code=201)
    def post(self):
        Department.query.get_or_404(ns.payload["department_id"], description="Department not found")
        course = Course(name=ns.payload["name"], department_id=ns.payload["department_id"])
        db.session.add(course)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Course name already exists")
        return course, 201


@ns.route("/courses/<int:id>")
class CourseAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(course_model)
    def get(self, id):
        return Course.query.get_or_404(id, description="Course not found")

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get_or_404(id, description="Course not found")
        Department.query.get_or_404(ns.payload["department_id"], description="Department not found")
        course.name = ns.payload["name"]
        course.department_id = ns.payload["department_id"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Course name already exists")
        return course

    @ns.expect(course_patch_model)
    @ns.marshal_with(course_model)
    def patch(self, id):
        course = Course.query.get_or_404(id, description="Course not found")
        if "name" in ns.payload:
            course.name = ns.payload["name"]
        if "department_id" in ns.payload:
            Department.query.get_or_404(ns.payload["department_id"], description="Department not found")
            course.department_id = ns.payload["department_id"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Course name already exists")
        return course

    def delete(self, id):
        course = Course.query.get_or_404(id, description="Course not found")
        db.session.delete(course)
        db.session.commit()
        return {}, 204


@ns.route("/courses/<int:id>/students")
class CourseStudentsAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(student_model)
    def get(self, id):
        Course.query.get_or_404(id, description="Course not found")
        enrolments = StudentEnrolment.query.filter_by(course_id=id).all()
        return [e.student for e in enrolments]


# --- Students ---

@ns.route("/students")
class StudentListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model, code=201)
    def post(self):
        student = Student(
            name=ns.payload["name"],
            email=ns.payload["email"],
            student_number=ns.payload["student_number"],
        )
        db.session.add(student)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Student name, email, or student number already exists")
        return student, 201


@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(student_model)
    def get(self, id):
        return Student.query.get_or_404(id, description="Student not found")

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get_or_404(id, description="Student not found")
        student.name = ns.payload["name"]
        student.email = ns.payload["email"]
        student.student_number = ns.payload["student_number"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Student name, email, or student number already exists")
        return student

    @ns.expect(student_patch_model)
    @ns.marshal_with(student_model)
    def patch(self, id):
        student = Student.query.get_or_404(id, description="Student not found")
        if "name" in ns.payload:
            student.name = ns.payload["name"]
        if "email" in ns.payload:
            student.email = ns.payload["email"]
        if "student_number" in ns.payload:
            student.student_number = ns.payload["student_number"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Student name, email, or student number already exists")
        return student

    def delete(self, id):
        student = Student.query.get_or_404(id, description="Student not found")
        db.session.delete(student)
        db.session.commit()
        return {}, 204


@ns.route("/students/<int:id>/courses")
class StudentCoursesAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(course_model)
    def get(self, id):
        Student.query.get_or_404(id, description="Student not found")
        enrolments = StudentEnrolment.query.filter_by(student_id=id).all()
        return [e.course for e in enrolments]


# --- Teachers ---

@ns.route("/teachers")
class TeacherListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(teacher_model)
    def get(self):
        return Teacher.query.all()

    @ns.expect(teacher_input_model)
    @ns.marshal_with(teacher_model, code=201)
    def post(self):
        teacher = Teacher(name=ns.payload["name"], email=ns.payload["email"])
        db.session.add(teacher)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Teacher name or email already exists")
        return teacher, 201


@ns.route("/teachers/<int:id>")
class TeacherAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(teacher_model)
    def get(self, id):
        return Teacher.query.get_or_404(id, description="Teacher not found")

    @ns.expect(teacher_input_model)
    @ns.marshal_with(teacher_model)
    def put(self, id):
        teacher = Teacher.query.get_or_404(id, description="Teacher not found")
        teacher.name = ns.payload["name"]
        teacher.email = ns.payload["email"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Teacher name or email already exists")
        return teacher

    @ns.expect(teacher_patch_model)
    @ns.marshal_with(teacher_model)
    def patch(self, id):
        teacher = Teacher.query.get_or_404(id, description="Teacher not found")
        if "name" in ns.payload:
            teacher.name = ns.payload["name"]
        if "email" in ns.payload:
            teacher.email = ns.payload["email"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "Teacher name or email already exists")
        return teacher

    def delete(self, id):
        teacher = Teacher.query.get_or_404(id, description="Teacher not found")
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204


@ns.route("/teachers/<int:id>/courses")
class TeacherCoursesAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(course_model)
    def get(self, id):
        Teacher.query.get_or_404(id, description="Teacher not found")
        enrolments = Enrolment.query.filter_by(teacher_id=id).all()
        return [e.course for e in enrolments]


# --- Enrolments (teacher-course) ---

@ns.route("/enrolments")
class EnrolmentListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(enrolment_model)
    def get(self):
        return Enrolment.query.all()

    @ns.expect(enrolment_input_model)
    @ns.marshal_with(enrolment_model, code=201)
    def post(self):
        Teacher.query.get_or_404(ns.payload["teacher_id"], description="Teacher not found")
        Course.query.get_or_404(ns.payload["course_id"], description="Course not found")
        enrolment = Enrolment(teacher_id=ns.payload["teacher_id"], course_id=ns.payload["course_id"])
        db.session.add(enrolment)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "This teacher is already assigned to this course")
        return enrolment, 201


@ns.route("/enrolments/<int:id>")
class EnrolmentAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(enrolment_model)
    def get(self, id):
        return Enrolment.query.get_or_404(id, description="Enrolment not found")

    def delete(self, id):
        enrolment = Enrolment.query.get_or_404(id, description="Enrolment not found")
        db.session.delete(enrolment)
        db.session.commit()
        return {}, 204


# --- Student Enrolments (student-course) ---

@ns.route("/student-enrolments")
class StudentEnrolmentListAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_list_with(student_enrolment_model)
    def get(self):
        return StudentEnrolment.query.all()

    @ns.expect(student_enrolment_input_model)
    @ns.marshal_with(student_enrolment_model, code=201)
    def post(self):
        Student.query.get_or_404(ns.payload["student_id"], description="Student not found")
        Course.query.get_or_404(ns.payload["course_id"], description="Course not found")
        se = StudentEnrolment(student_id=ns.payload["student_id"], course_id=ns.payload["course_id"])
        db.session.add(se)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ns.abort(409, "This student is already enrolled in this course")
        return se, 201


@ns.route("/student-enrolments/<int:id>")
class StudentEnrolmentAPI(Resource):
    method_decorators = [token_required]

    @ns.marshal_with(student_enrolment_model)
    def get(self, id):
        return StudentEnrolment.query.get_or_404(id, description="Student enrolment not found")

    def delete(self, id):
        se = StudentEnrolment.query.get_or_404(id, description="Student enrolment not found")
        db.session.delete(se)
        db.session.commit()
        return {}, 204
