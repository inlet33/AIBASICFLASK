from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addstudent')
def addstudent():
    return render_template('student/studentadd.html')

@app.route('/student')
def student():
    student_list= [
        {'name':'jan', 'age':25, 'address':'Cebu' },
        {'name':'chika', 'age':25, 'address':'Cebu' },
        {'name':'hiro', 'age':25, 'address':'Cebu' },
        {'name':'asuka', 'age':25, 'address':'Cebu' }
    ]
    return render_template('student/studentlist.html',students = student_list)

@app.route('/addteacher')
def addteacher():
    return render_template('teacher/teacheradd.html')

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
    return render_template('schedule/scheduleadd.html')

@app.route('/schedule')
def schedule():
    schedule_list= []
    return render_template('schedule/schedulelist.html',schedules = schedule_list)

@app.route('/addsubject')
def addsubject():
    return render_template('subject/subjectadd.html')

@app.route('/subject')
def subject():
    subject_list= []
    return render_template('subject/subjectlist.html',subjects = subject_list)

@app.route('/addcourse')
def addcourse():
    return render_template('course/courseadd.html')

@app.route('/course')
def course():
    course_list= []
    return render_template('course/courselist.html',courses = course_list)


if __name__ == "__main__":
    app.run(debug = True)