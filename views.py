from .app import app
from .database import db
from flask import Flask,render_template, request,redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField,BooleanField,SelectField
import os
from .models.models import Student,Teacher,Course,Subject


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
        student = Student(name=request.form['studentname'],age=request.form['studentage'],address=request.form['studentaddress'])
        db.session.add(student)
        db.session.commit()
        return redirect('/student')
        # if int(request.form["studentage"]) >= 18:
        #     return "welcome to flask {}".format(request.form["studentname"])
        # else:
        #     return "you are not allowed {}".format(request.form["studentname"])
    return render_template('student/studentadd.html',form = form)

@app.route('/student')
def student():
    student_list=Student.query.all()
    return render_template('student/studentlist.html',students = student_list)

@app.route('/studentdelete/<int:student_id>')
def studentdelete(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/student')

@app.route('/studentupdate/<int:student_id>',methods=['GET','POST'])
def studentupdate(student_id):
    student = Student.query.get(student_id)
    
    if request.method == 'POST':
        student.name = request.form['student_name']
        student.age = request.form['student_age']
        student.address = request.form['student_address']
        db.session.commit()
        return redirect('/student')

    return render_template('student/studentupdate.html',student = student)


@app.route('/addteacher',methods= ['GET', 'POST'])
def addteacher():
    form =TeacherForm()
    if request.method == 'POST':
        teacher = Teacher(name=request.form['teachername'],age=request.form['teacherage'],address=request.form['teacheraddress'])
        db.session.add(teacher)
        db.session.commit()
        return redirect('/teacher')
    return render_template('teacher/teacheradd.html',form = form)


@app.route('/teacher')
def teacher():
    teacher_list= Teacher.query.all()
    return render_template('teacher/teacherlist.html',teachers = teacher_list)

@app.route('/teacherdelete/<int:teacher_id>')
def teacherdelete(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect('/teacher')

@app.route('/teacherupdate/<int:teacher_id>',methods=['GET','POST'])
def teacherupdate(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    
    if request.method == 'POST':
        teacher.name = request.form['teacher_name']
        teacher.age = request.form['teacher_age']
        teacher.address = request.form['teacher_address']
        db.session.commit()
        return redirect('/teacher')

    return render_template('teacher/teacherupdate.html',teacher = teacher)



@app.route('/addschedule')
def addschedule():
    form = ScheduleForm()
    return render_template('schedule/scheduleadd.html',form = form)

@app.route('/schedule')
def schedule():
    schedule_list= []
    return render_template('schedule/schedulelist.html',schedules = schedule_list)



@app.route('/addsubject',methods= ['GET', 'POST'])
def addsubject():
    form = SubjectForm()
    if request.method == 'POST':
        subject = Subject(name=request.form['subjectname'],code=request.form['subjectcode'])
        db.session.add(subject)
        db.session.commit()
        return redirect('/subject')
    return render_template('subject/subjectadd.html',form = form)



@app.route('/subject')
def subject():
    subject_list= Subject.query.all()
    return render_template('subject/subjectlist.html',subjects = subject_list)

@app.route('/subjectdelete/<int:subject_id>')
def subjectdelete(subject_id):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect('/subject')

@app.route('/subjectupdate/<int:subject_id>',methods=['GET','POST'])
def subjectupdate(subject_id):
    subject = Subject.query.get(subject_id)
    
    if request.method == 'POST':
        subject.name = request.form['subject_name']
        subject.code = request.form['subject_code']
        db.session.commit()
        return redirect('/subject')

    return render_template('subject/subjectupdate.html',subject = subject)

@app.route('/addcourse',methods= ['GET', 'POST'])
def addcourse():
    form = CourseForm()
    if request.method == 'POST':
        course = Course(name=request.form['coursename'],code=request.form['coursecode'])
        db.session.add(course)
        db.session.commit()
        return redirect('/course')
    return render_template('course/courseadd.html',form = form)

@app.route('/course')
def course():
    course_list= Course.query.all()
    return render_template('course/courselist.html',courses = course_list)

@app.route('/coursedelete/<int:course_id>')
def coursedelete(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect('/course')

@app.route('/courseupdate/<int:course_id>',methods=['GET','POST'])
def courseupdate(course_id):
    course = Course.query.get(course_id)
    
    if request.method == 'POST':
        course.name = request.form['course_name']
        course.code = request.form['course_code']
        db.session.commit()
        return redirect('/course')

    return render_template('course/courseupdate.html',course = course)
