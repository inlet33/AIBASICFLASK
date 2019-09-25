from datetime import datetime
from AIBASICFLASK.database import db
from sqlalchemy.orm import relationship

class Student(db.Model): 

    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(245))
    student_type = db.Column(db.String(45))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    enrollments =db.relationship("Enrollment",back_populates = 'students')

    @staticmethod
    def search_student(name):
        return db.session.query(Student).filter(Student.name == name).all()

class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(245))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    schedules = db.relationship("Schedule",back_populates='teachers')

    @staticmethod
    def search_teacher(name):
        return db.session.query(Teacher).filter(Teacher.name == name).all()

class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    schedules = db.relationship("Schedule",back_populates='courses')
    course_sections = db.relationship("CourseSection",back_populates='courses')


    def __init__(self,name,code):
        self.name = name
        self.code = code

    def check_course_exist(self,name,code):
        return db.session.query(Course).filter(Course.name == name).filter(Course.code == code).all()

    @staticmethod
    def search_course(code):
        return db.session.query(Course).filter(Course.code == code).all()

class CourseSection(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    courses =db.relationship("Course",back_populates = 'course_sections')
    schedules = db.relationship("Schedule",back_populates='course_sections')


class Subject(db.Model):

    __tablename__ = 'subjects'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45),)
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    schedules =db.relationship("Schedule",back_populates = 'subjects')

    def __init__(self,name,code):
        self.name = name
        self.code = code

    def check_subject_exist(self,name,code):
        return db.session.query(Subject).filter(Subject.name == name).filter(Subject.code == code).all()

    @staticmethod
    def search_subject(code):
        return db.session.query(Subject).filter(Subject.code == code).all()

class Schedule(db.Model):

    __tablename__ = 'schedules'

    id = db.Column(db.Integer,primary_key = True)
    start = db.Column(db.String(45), nullable = False)
    end = db.Column(db.String(45), nullable = False)
    day =db.Column(db.String(45), nullable = False)
    course =db.Column(db.Integer,db.ForeignKey('courses.id'))
    teacher =db.Column(db.Integer,db.ForeignKey('teachers.id'))
    section_id =db.Column(db.Integer,db.ForeignKey('course_sections.id'))
    subject_id =db.Column(db.Integer,db.ForeignKey('subjects.id'))
    term = db.Column(db.String(45), nullable = False)
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    courses =db.relationship("Course",back_populates = 'schedules')
    teachers =db.relationship("Teacher",back_populates = 'schedules')
    enrollments =db.relationship("Enrollment",back_populates = 'schedules')
    course_sections =db.relationship("CourseSection",back_populates = 'schedules')
    subjects =db.relationship("Subject",back_populates = 'schedules')


    def __init__(self,start,end,day,teacher,section_id, subject_id,term):
        self.start = start
        self.end = end
        self.day = day
        #self.course = course
        self.teacher = teacher
        self.section_id = section_id
        self.subject_id = subject_id
        self.term = term

    def check_schedule_exist(self,start,teacher):
        return db.session.query(Schedule).filter(Schedule.start == start).filter(Schedule.teacher == teacher).all()

    @staticmethod
    def search_schedule(day):
        return db.session.query(Schedule).filter(Schedule.day == day).all()

class Enrollment(db.Model):

    __tablename__ = 'enrollments'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45),db.ForeignKey('students.id')) 
    date = db.Column(db.String(45),db.ForeignKey('schedules.id'))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    students =db.relationship("Student",back_populates = 'enrollments')
    schedules =db.relationship("Schedule",back_populates = 'enrollments')

    def __init__(self,name,date):
        self.name = name
        self.date = date

    def check_enrollment_exist(self,date,term):
        return db.session.query(Enrollment).filter(Enrollment.date == date).filter(Enrollment.term == term).all()

    @staticmethod
    def search_enrollment(name):
        return db.session.query(Enrollment).filter(Enrollment.name == name).all()

