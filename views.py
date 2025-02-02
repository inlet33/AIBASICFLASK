from .app import app
from .database import db
from flask import Flask,render_template, request,redirect,flash, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms_components import TimeField,DateField,DateTimeField, SelectMultipleField
from wtforms import StringField, PasswordField,BooleanField,SelectField,DateTimeField
from wtforms.validators import InputRequired, Email, Length
import os
from .models.models import Student,Teacher,Course,Subject,Schedule,Enrollment,CourseSection,User
from wtforms.widgets import ListWidget,CheckboxInput
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

#Initialize LoginManager to use it's functions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class RegisterForm(FlaskForm):
    username = StringField("Username", validators =[InputRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators= [InputRequired(), Email(message="Invalid Email")])
    password = PasswordField("Password" , validators=[InputRequired(), Length(min=4 ,max=12)])
    role = SelectField("User Role", choices=[('user','user'),('admin','admin')])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class MultiCheckBoxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class StudentForm(FlaskForm):
    studentname = StringField("Student Name")
    studentage = StringField("Student Age")
    studentaddress = StringField("Student Adress")
    studenttype = SelectField("Type",choices=[('regular','irregular')])
    studentyear = SelectField("Student Year LVL",choices=[('1','1st Year'),('2','2nd Year'),('3','3rd Year'),('4','4th Year')])

class TeacherForm(FlaskForm):
    teachername = StringField("Teacher Name")
    teacherage = StringField("Teacher Age")
    teacheraddress = StringField("Teacher Adress")

class CourseForm(FlaskForm):
    coursename = StringField("Course Name")
    coursecode = StringField("Course Code")

class Course_SectionForm(FlaskForm):
    coursesectionname = StringField("Course Section Name")
    coursesectioncode = StringField("Course Section Code")
    coursesectioncourse = SelectField("Course Section Course",choices=[])

class SubjectForm(FlaskForm):
    subjectname = StringField("Subject Name")
    subjectcode = StringField("Subject Code")

class ScheduleForm(FlaskForm):
    schedulestarttime = TimeField("Start Time")
    scheduleendtime = TimeField("End Time")
    scheduleday = SelectField("Day",choices=[('M-F','M-F')])
    course = SelectField("Course",choices=[])
    teacher = SelectField("Teacher",choices=[])
    schdulecoursesection = SelectField("Course Section",choices=[])
    schdulesubject = SelectField("Subject",choices=[])
    scheduleterm = SelectField("Term",choices=[('term 1','term 1'),('term 2','term 2')])

class EnrollmentForm(FlaskForm):
    enrollmentname = SelectField("Student Name",choices=[])
    enrollmentdate = SelectField("Schedule Date",choices=[])
    enrollmentcourse = SelectField("Course",choices=[])
    enrollmentcoursesection = SelectField("Course Section",choices=[])
    enrollmentterm = SelectField("Term",choices=[("term 1","term 1"),("term 2","term 2")])
    # #Get the values using choice(schedule_id, subject_name) example:(1, IT)
    # schedule =MultiCheckBoxField('schdule')

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

#Load the user information after logging in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Register Form
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()

    #check if all the validators is successful
    if form.validate_on_submit():
        #encryupt the password before saving in the database
        hashed_password = generate_password_hash(request.form['password'],method="sha256")
        user = User(username = request.form['username'],
                    email= request.form['email'],
                    password=hashed_password,
                    role= request.form['role'])
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect('/student')
    return render_template('auth/register.html', form = form)

#Login Form
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            user = User.query.filter(User.username == request.form['username']).first()
            if user:
                if check_password_hash(user.password, request.form['password']):
                    login_user(user)
                    return redirect('/enrollment')
                else:
                    flash('Invalid Password', 'error')
            else:
                flash('Invalid Username or Password', 'error')
    return render_template('auth/login.html', form = form)

#Logout function
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/userlist')
@login_required
def user():
    users = User.query.all()

    return render_template('auth/userlist.html', users = users)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addstudent', methods= ['GET', 'POST'])
@login_required

def addstudent():
    form =StudentForm()
    if request.method == 'POST':
        student = Student(name=request.form['studentname'],age=request.form['studentage'],address=request.form['studentaddress'],student_type=request.form['studenttype'])
        db.session.add(student)
        db.session.commit()
        return redirect('/student')
        # if int(request.form["studentage"]) >= 18:
        #     return "welcome to flask {}".format(request.form["studentname"])
        # else:
        #     return "you are not allowed {}".format(request.form["studentname"])
    return render_template('student/studentadd.html',form = form, user=current_user)

@app.route('/student', methods=['GET','POST'])
@login_required

def student():
    student_list=Student.query.all()
    if request.method == 'POST':
        search = Student.search_student(request.form['search'])
        return render_template('student/studentlist.html',teachers = search)
    return render_template('student/studentlist.html',students = student_list,user=current_user)

@app.route('/studentdelete/<int:student_id>')
@login_required

def studentdelete(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/student')

@app.route('/studentupdate/<int:student_id>',methods=['GET','POST'])
@login_required
def studentupdate(student_id):
    student = Student.query.get(student_id)
    
    if request.method == 'POST':
        student.name = request.form['student_name']
        student.age = request.form['student_age']
        student.address = request.form['student_address']
        db.session.commit()
        return redirect('/student')

    return render_template('student/studentupdate.html',student = student)

@app.route('/studentschedule/<int:student_id>')
@login_required
def studentschedule(student_id):
    student = Student.query.get(student_id)
    
    return render_template('student/studentschedule.html',student = student,user=current_user)

@app.route('/addteacher',methods= ['GET', 'POST'])
@login_required
def addteacher():
    form =TeacherForm()
    if request.method == 'POST':
        teacher = Teacher(name=request.form['teachername'],age=request.form['teacherage'],address=request.form['teacheraddress'])
        db.session.add(teacher)
        db.session.commit()
        return redirect('/teacher')
    return render_template('teacher/teacheradd.html',form = form,user=current_user)

@app.route('/teacher', methods=['GET','POST'])
@login_required
def teacher():
    teacher_list= Teacher.query.all()
    if request.method == 'POST':
        search = Teacher.search_teacher(request.form['search'])
        return render_template('teacher/teacherlist.html',teachers = search)
    return render_template('teacher/teacherlist.html',teachers = teacher_list,user=current_user)

@app.route('/teacherdelete/<int:teacher_id>')
@login_required
def teacherdelete(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect('/teacher')

@app.route('/teacherupdate/<int:teacher_id>',methods=['GET','POST'])
@login_required
def teacherupdate(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    
    if request.method == 'POST':
        teacher.name = request.form['teacher_name']
        teacher.age = request.form['teacher_age']
        teacher.address = request.form['teacher_address']
        db.session.commit()
        return redirect('/teacher')

    return render_template('teacher/teacherupdate.html',teacher = teacher)

@app.route('/teacherschedule/<int:teacher_id>')
@login_required
def teacherschedule(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    
    return render_template('teacher/teacherschedule.html',teacher = teacher,user=current_user)

@app.route('/addschedule',methods=['GET','POST'])
@login_required
def addschedule():
    form = ScheduleForm()
    form.schdulecoursesection.choices = [(coursesection.id,coursesection.name)for coursesection in CourseSection.query.all()]
    form.teacher.choices = [(teacher.id,teacher.name)for teacher in Teacher.query.all()]
    form.schdulesubject.choices = [(subject.id,subject.name)for subject in Subject.query.all()]

    if request.method == 'POST':
        schedule = Schedule(start=request.form['schedulestarttime'],
        end=request.form['scheduleendtime'],
        day=request.form['scheduleday'],
        term = request.form['scheduleterm'],
        section_id=request.form['schdulecoursesection'],
        subject_id=request.form['schdulesubject'],
        teacher=request.form['teacher'])

        check1 =schedule.check_schedule_exist(start=request.form['schedulestarttime']
        ,end=request.form['scheduleendtime']
        ,term =request.form['scheduleterm']
        ,section_id =request.form['schdulecoursesection'])

        check2 =schedule.check_class_subject_exist(term =request.form['scheduleterm']
        ,section_id =request.form['schdulecoursesection']
        ,subject_id =request.form['schdulesubject'])

        if len(check1) ==0:
            if len(check2) ==0:             
                db.session.add(schedule)
                db.session.commit()
                return redirect('/schedule')
        # flash('Schedule already exist','error')
        return redirect('/addschedule')
    return render_template('schedule/scheduleadd.html',form = form,user=current_user)

@app.route('/schedule', methods=['GET','POST'])
@login_required
def schedule():
    schedule_list= db.session.query(Schedule).join(CourseSection,CourseSection.id ==Schedule.section_id).all() 
    if request.method == 'POST':
        search = Schedule.search_schedule(request.form['search'])
        return render_template('schedule/schedulelist.html',schedules = search)
    return render_template('schedule/schedulelist.html',schedules = schedule_list,user=current_user)

@app.route('/scheduledelete/<int:schedule_id>')
@login_required
def scheduledelete(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect('/schedule')

@app.route('/scheduleupdate/<int:schedule_id>',methods=['GET','POST'])
@login_required
def scheduleupdate(schedule_id):
    # form = ScheduleForm()
    # schedule = Schedule.query.get(schedule_id)
    # form.schedulestarttime.data = schedule.start
    # form.scheduleendtime.data = schedule.end
    # form.scheduleday.choices = [(schedule.id,schedule.day)for schedule in Schedule.query.all()]
    # form.course.choices = [(course.id,course.name)for course in Course.query.all()]
    # form.teacher.choices = [(teacher.id,teacher.name)for teacher in Teacher.query.all()]
    
    
    # if request.method == 'POST':
    #     schedule = Schedule(start=request.form['schedulestarttime'],
    #     end=request.form['scheduleendtime'],
    #     day=request.form['scheduleday'],
    #     course=request.form['course'],
    #     teacher=request.form['teacher'])
    #     check =schedule.check_schedule_exist(request.form['schedulestarttime'],teacher =request.form['teacher'])
    #     if len(check) ==0:
    #         db.session.add(schedule)
    #         db.session.commit()
    #         return redirect('/schedule')
    #     flash('Schedule already exist','error')
    #     return redirect('/addschedule')
    
    # return render_template('schedule/scheduleadd.html',form = form)
    schedule = Schedule.query.get(schedule_id)
    
    if request.method == 'POST':
        schedule.start = request.form['schedule_start']
        schedule.end = request.form['schedule_end']
        schedule.day = request.form['schedule_day']
        schedule.course = request.form['schedule_course']
        schedule.teacher = request.form['schedule_teacher']
        db.session.commit()
        return redirect('/schedule')

    return render_template('schedule/scheduleupdate.html',schedule = schedule)

@app.route('/addsubject',methods= ['GET', 'POST'])
@login_required
def addsubject():
    form = SubjectForm()
    if request.method == 'POST':
        subject = Subject(name=request.form['subjectname'],code=request.form['subjectcode'])
        check =subject.check_subject_exist(request.form['subjectname'],request.form['subjectcode'])
        if len(check) ==0:
            db.session.add(subject)
            db.session.commit()
            return redirect('/subject')
        return redirect('/addsubject')
    return render_template('subject/subjectadd.html',form = form,user=current_user)

@app.route('/subject', methods=['GET','POST'])
@login_required
def subject():
    subject_list= Subject.query.all()
    if request.method == 'POST':
        search = Subject.search_subject(request.form['search'])
        return render_template('subject/subjectlist.html',subjects = search)
    return render_template('subject/subjectlist.html',subjects = subject_list,user=current_user)

@app.route('/subjectdelete/<int:subject_id>')
@login_required
def subjectdelete(subject_id):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect('/subject')

@app.route('/subjectupdate/<int:subject_id>',methods=['GET','POST'])
@login_required
def subjectupdate(subject_id):
    subject = Subject.query.get(subject_id)
    
    if request.method == 'POST':
        subject.name = request.form['subject_name']
        subject.code = request.form['subject_code']
        db.session.commit()
        return redirect('/subject')

    return render_template('subject/subjectupdate.html',subject = subject)

@app.route('/addcourse',methods= ['GET', 'POST'])
@login_required
def addcourse():
    form = CourseForm()
    if request.method == 'POST':
        course = Course(name=request.form['coursename'],code=request.form['coursecode'])
        check =course.check_course_exist(request.form['coursename'],request.form['coursecode'])
        if len(check) ==0:
            db.session.add(course)
            db.session.commit()
            return redirect('/course')
        return redirect('/addcourse')
    return render_template('course/courseadd.html',form = form,user=current_user)

@app.route('/course', methods=['GET','POST'])
@login_required
def course():
    course_list= Course.query.all()
    if request.method == 'POST':
        search = Course.search_course(request.form['search'])
        return render_template('course/courselist.html',courses = search)
    return render_template('course/courselist.html',courses = course_list,user=current_user)

@app.route('/coursedelete/<int:course_id>')
@login_required
def coursedelete(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect('/course')

@app.route('/courseupdate/<int:course_id>',methods=['GET','POST'])
@login_required
def courseupdate(course_id):
    course = Course.query.get(course_id)
    
    if request.method == 'POST':
        course.name = request.form['course_name']
        course.code = request.form['course_code']
        db.session.commit()
        return redirect('/course')

    return render_template('course/courseupdate.html',course = course)

@app.route('/courseschedule/<int:course_id>')
@login_required
def courseschedule(course_id):
    course = Course.query.get(course_id)
    
    return render_template('course/courseschedule.html',course = course,user=current_user)

@app.route('/addenrollment',methods= ['GET', 'POST'])
@login_required
def addenrollment():
    form = EnrollmentForm()
    form.enrollmentname.choices = [(student.id,student.name)for student in Student.query.all()]
    form.enrollmentcourse.choices = [(course.id,course.name)for course in Course.query.all()]

    if request.method == 'POST':
        course_id = request.form['enrollmentcourse']
        student_id = request.form['enrollmentname']
        return redirect(url_for('enrollment_section',course_id=course_id,student_id=student_id))   
    return render_template('enrollment/enrollmentadd.html',form = form,user=current_user)

@app.route('/enrollmentcoursesection', methods = ['GET', 'POST'])
@login_required
def enrollment_section():
    form = EnrollmentForm()
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')
    form.enrollmentcoursesection.choices=[(course.id,course.name)for course in CourseSection.query.filter(CourseSection.course_id == course_id).all()]
    if request.method == 'POST':
        section_id = request.form['enrollmentcoursesection']
        term = request.form['enrollmentterm']
        return redirect(url_for('enrollment_schdeule',student_id=student_id,section_id =section_id, term= term ))
    return render_template('enrollment/enrollmentcoursesection.html',form = form,student_id=student_id,user=current_user)

@app.route('/enrollmentschedule', methods = ['GET', 'POST'])
@login_required
def enrollment_schdeule():
    schedules = Schedule.query.filter_by(section_id = request.args.get('section_id')).filter_by(term = request.args.get('term'))
    student = Student.query.filter_by(id =request.args.get('student_id'))

    if request.method == 'POST':
        for schedule in schedules:
            enrollment = Enrollment(student_id=request.args.get('student_id'),
                                    schedule_id=schedule.id,
                                    start_year = datetime.date.today().year,
                                    end_year = datetime.date.today().year+1)
            db.session.add(enrollment)
            db.session.commit()
        return redirect('/enrollment')

    return render_template('enrollment/enrollmentschedule.html',schedules = schedules,student=student,user=current_user)

@app.route('/enrollment', methods=['GET','POST'])
@login_required
def enrollment():
    students= Student.query.join(Enrollment,Student.id ==Enrollment.student_id).all() 
  
    return render_template('enrollment/enrollmentlist.html',user=current_user,students = students)

@app.route('/enrollmentview/<int:student_id>', methods=['GET','POST'])
@login_required
def enrollmentview(student_id):
    enrollments = Enrollment.query.filter(Enrollment.student_id ==student_id)
    enrollments_years = Enrollment.query.filter(Enrollment.student_id ==student_id)

    return render_template('enrollment/enrollmentview.html',enrollments=enrollments,user=current_user,enrollments_years= enrollments_years)

@app.route('/enrollmentdelete/<int:enrollment_id>')
@login_required
def enrollmentdelete(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    return redirect('/enrollment')

@app.route('/enrollmentupdate/<int:enrollment_id>',methods=['GET','POST'])
@login_required
def enrollmentupdate(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id).all()
    
    if request.method == 'POST':
        enrollment.name = request.form['enrollment_name']
        enrollment.date = request.form['enrollment_date']
        enrollment.term = request.form['enrollment_term']
        db.session.commit()
        return redirect('/enrollment')

    return render_template('enrollment/enrollmentupdate.html',enrollment = enrollment)

@app.route('/addcoursesection',methods= ['GET', 'POST'])
@login_required
def addcourse_section():
    form = Course_SectionForm()
    form.coursesectioncourse.choices = [(course.id, course.name)for course in Course.query.all()]

    if request.method == 'POST':
        course_section = CourseSection(name=request.form['coursesectionname'],code=request.form['coursesectioncode'],course_id=request.form['coursesectioncourse'])
        db.session.add(course_section)
        db.session.commit()
        # check =course.check_course_exist(request.form['coursesectionname'],request.form['coursesectionncode'])
        # if len(check) ==0:
        #     db.session.add(course_section)
        #     db.session.commit()
        return redirect('/course_section')
        #return redirect('/addcoursesection')
    return render_template('course_section/course_sectionadd.html',form = form,user=current_user)

@app.route('/course_section', methods=['GET','POST'])
@login_required
def course_section():
    course_section_list= CourseSection.query.all()
    return render_template('course_section/course_sectionlist.html',coursesections = course_section_list,user=current_user)

@app.route('/coursesectiondelete/<int:coursesections_id>')
@login_required
def course_sectiondelete(coursesections_id):
    course = CourseSection.query.get(coursesections_id)
    db.session.delete(course)
    db.session.commit()
    return redirect('/course_section')

# @app.route('/coursesectionsupdate/<int:course_id>',methods=['GET','POST'])
# def courseupdate(course_id):