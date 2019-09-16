from datetime import datetime
from AIBASICFLASK.database import db

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,nullable= False, default = datetime.now)
    updated_at = db.Column(db.DateTime,nullable= False, default = datetime.now,onupdate = datetime.now)
