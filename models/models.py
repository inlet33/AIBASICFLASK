from datetime import datetime
from AIBASICFLASK.database import db

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


class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

class Subject(db.Model):

    __tablename__ = 'subject'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    code = db.Column(db.String(45))
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)

# class Schedule(db.Model):

#     __tablename__ = 'schedule'

#     id = db.Column(db.Integer,primary_key = True)
#     day_schedule = db.Column(db.String(45), nullable = False)
#     time_schedule_from = db.Column(db.)
#     time_schedule_to = db.Column(db.)
#     course_id =db.Column(db.Integer)
#     subject_id =db.Column(db.Integer)
#     teacher_id =db.Column(db.Integer)
#     created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
#     updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)