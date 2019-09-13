from flask import Flask,render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField,BooleanField,SelectField
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bootstrap = Bootstrap(app)

class StudentForm(FlaskForm):
    studentname = StringField("Student Name")
    studentage = StringField("Student Age")
    studentaddress = StringField("Student Adress")
    studentyear = SelectField("Student Year LVL",choices=[('1','1st Year'),('2','2nd Year'),('3','3rd Year'),('4','4th Year')])

class TeacherForm(FlaskForm):
    teachername = StringField("Teacher Name")
    teacherage = StringField("Teacher Age")
    teacheraddress = StringField("Teacher Adress")

class CourseForm(FlaskForm):
    coursename = StringField("Course Name")
    coursecode = StringField("Course Code")

class SubjectForm(FlaskForm):
    subjectname = StringField("Subject Name")
    subjectcode = StringField("Subject Code")

class ScheduleForm(FlaskForm):
    schedulename = StringField("Schedule Name")
    schedulecode = StringField("Schedule Code")



@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addstudent', methods= ['GET', 'POST'])
def addstudent():
    form =StudentForm()
    if request.method == 'POST':
        if int(request.form["studentage"]) >= 18:
            return "welcome to flask {}".format(request.form["studentname"])
        else:
            return "you are not allowed {}".format(request.form["studentname"])
    return render_template('student/studentadd.html',form = form)

@app.route('/student')
def student():
    student_list= [
        {'name':'jan', 'age':25, 'address':'Cebu' },
        {'name':'chika', 'age':25, 'address':'Cebu' },
        {'name':'hiro', 'age':25, 'address':'Cebu' },
        {'name':'asuka', 'age':25, 'address':'Cebu' }
    ]
    return render_template('student/studentlist.html',students = student_list)

@app.route('/addteacher',methods= ['GET', 'POST'])
def addteacher():
    form =TeacherForm()
    return render_template('teacher/teacheradd.html',form = form)

@app.route('/teacher')
def teacher():
    teacher_list= [
        # {'name':'jan', 'age':25, 'address':'Cebu' },
        # {'name':'chika', 'age':25, 'address':'Cebu' },
        # {'name':'hiro', 'age':25, 'address':'Cebu' },
        # {'name':'asuka', 'age':25, 'address':'Cebu' }
    ]
    return render_template('teacher/teacherlist.html',teachers = teacher_list)

@app.route('/addschedule')
def addschedule():
    form = ScheduleForm()
    return render_template('schedule/scheduleadd.html',form = form)

@app.route('/schedule')
def schedule():
    schedule_list= []
    return render_template('schedule/schedulelist.html',schedules = schedule_list)

@app.route('/addsubject')
def addsubject():
    form = SubjectForm()
    return render_template('subject/subjectadd.html',form = form)

@app.route('/subject')
def subject():
    subject_list= []
    return render_template('subject/subjectlist.html',subjects = subject_list)

@app.route('/addcourse')
def addcourse():
    form = CourseForm()
    return render_template('course/courseadd.html',form = form)

@app.route('/course')
def course():
    course_list= []
    return render_template('course/courselist.html',courses = course_list)


if __name__ == "__main__":
    app.run(debug = True)