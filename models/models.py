from datetime import datetime
from AIBASICFLASK.database import db
from sqlalchemy.orm import relationship

class Student(db.Model): #just difined, it is called at models/__init__.py

    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(245))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(245))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    schedules = db.relationship("Schedule",back_populates='teachers')

class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    schedules = db.relationship("Schedule",back_populates='courses')

class Subject(db.Model):

    __tablename__ = 'subject'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45),)
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

class Schedule(db.Model):

    __tablename__ = 'schedule'

    id = db.Column(db.Integer,primary_key = True)
    start = db.Column(db.String(45), nullable = False)
    end = db.Column(db.String(45), nullable = False)
    day =db.Column(db.String(45), nullable = False)
    course =db.Column(db.Integer,db.ForeignKey('courses.id'))
    teacher =db.Column(db.Integer,db.ForeignKey('teachers.id'))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

    courses =db.relationship("Course",back_populates = 'schedules')
    teachers =db.relationship("Teacher",back_populates = 'schedules')