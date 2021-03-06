import datetime
import json
from flask import Flask, make_response, request, url_for, jsonify, render_template, request, redirect, session , escape, g
import MySQLdb
from flask.ext.httpauth import HTTPBasicAuth
import os
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from werkzeug import BaseResponse
from sqlalchemy import create_engine
from sqlalchemy import text
from functools import wraps
from Models import db
from Models import *
from flask.ext.login import login_user, logout_user, current_user, \
    login_required, LoginManager

UPLOAD_FOLDER = '/home/shubham/Desktop/web_development/tutplus/data/user_dp/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://13CS30030:cse12@10.5.18.68/13CS30030"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
# login_serializer = URLSafeTimedSerializer(app.secret_key)

login_manager.init_app(app)
with app.app_context():
    db.create_all()



@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(int(user_id))

def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:

    @template_or_json('template.html')

    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated


# Home API
@app.route("/" , methods = ['GET', 'POST'])
def home():
    return render_template('login.html')


# API for login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            print("error")
            return redirect(url_for('login'))
        email_ = json_data['email']
        pwd = json_data['password']

        print email_, pwd

        if g.user is not None and g.user.is_authenticated:
            print "shouldnt hppen"
            return redirect(url_for('profile'))

        user = User.query.filter_by(email = email_).first()
        print "IN LOGIN"

        if user and user.check_password(pwd):
            # session['email'] = email_
            session['user_id'] = user.user_id
            USERID = user.user_id
            session.modified = True
            print "In profile redirect"
            return redirect(url_for('profile'))
        else:
            print "IN login wala !! "
            return redirect(url_for('login'))

    if request.method == 'GET':
        print "get h"
        return render_template('login.html')


@app.route('/student', methods = ['GET'])
def student():
    return render_template('student.html')

@app.route('/signUp', methods = ['GET','POST'])
def add_user():
    if request.method == 'POST':
        json_data = request.get_json(force=True)

        if not json_data:
            print("error")
            return redirect(url_for('add_user'))
        name = json_data['name']
        email = json_data['email']
        pwd = json_data['password']
        DOB = str(json_data['dob'])
        print "*****" + pwd
        link = "link"
        flag = json_data['flag']
        newuser = User(name, email, pwd, link, flag , DOB)

        session['email'] = email
        db.session.add(newuser)
        session['user_id'] = name
        db.session.commit()

        user = User.query.filter_by(email = (session['email'])).first()
        if flag == 2:
            newfac = Faculty(user.user_id)
            db.session.add(newfac)
            db.session.commit()
        elif flag == 0:
            newadm = Admin(user.user_id)
            db.session.add(newadm)
            db.session.commit()
        elif flag == 1:
            newst = Student(user.user_id)
            db.session.add(newst)
            db.session.commit()


        return redirect(url_for('profile'), 302)

    if request.method == 'GET':
        return render_template('signup.html')

@app.route('/parentPortal', methods = ['GET' , 'POST'])
def parentPortal():
    if request.method == 'POST' :
        json_data = request.get_json(force = True)
        if not json_data :
            print ("Error !! No credentials Given !! ")
            return redirect(url_for('parentPortal'))
        rollno = json_data['RollNo']
        _email = json_data['Email']
        user = User.query.filter_by(user_id = rollno)
        if user is None or user.email != _email :
        	print("Sorry Wrong Credentials !! ")
        	return redirect(url_for('parentPortal'))
        else:
        	Performance = Performance_Sheet.query.filter_by(Student_Id = rollno)
        	return render_template('Parent_Portal.html')


@app.route('/forgotPassword', methods = ['GET' , 'POST'])
def forgotPassword():
	if request.method == 'POST' :j
        json_data = request.get_json(force = True)
        if not json_data :
            print ("Error !! No credentials Given !! ")
            return redirect(url_for('forgotPassword'))
    	rollno = json_data['RollNo']
        _email = json_data['Email']
        user = User.query.filter_by(user_id = rollno)
        if user is None or user.email != _email :
            print("Sorry Wrong Credentials !! ")
            return redirect(url_for('forgotPassword'))
        else:
            password = user.password
            context = {
            'Password' : password
            }
            return context


@app.route('/profile', methods=['GET', 'POST'])
@template_or_json('profile.html')
def profile():
    if g is None:
        return redirect(url_for('signup'))
    else:
        return ({'redirect': 'True', 'link' : '/profile'})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# API for searching a course
@app.route('/searchresults', methods = ['GET','POST'])
def search_course():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            print("error")
            return redirect(url_for('search_course'))
        cid = json_data['course_id']

        course = Course.query.filter_by(course_id = cid).first()

        if course:
            session['course_id'] = cid
            return redirect(url_for('course_home'))
        else:
            return redirect(url_for('search_course'))
            # session['email'] = email

    if request.method == 'GET':
        return render_template('student_home.html')


# API for enrolling a student in a course
@app.route('/enroll')
def enroll():
    newenroll = Enrolls(session['user_id'],session['course_id'])
    db.session.add(newenroll)
    db.session.commit()
    return redirect(url_for('course_home'), 302)


# API to add a new notice
@app.route('/addnotice', methods = ['GET','POST'])
def add_notice():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            print("error")
            return redirect(url_for('search_course'))
        cid = json_data['c_id']
        msg = json_data['message']

        newnotice = Notice(cid,msg)
        db.session.add(newnotice)
        db.session.commit()
        return redirect(url_for('course_home'), 302)


# API to add a new course
@app.route('/addcourse', methods = ['GET','POST'])
def add_course():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            print("error")
            return redirect(url_for('search_course'))
        cid = json_data['c_id']
        cname = json_data['course_name']
        pre = json_data['prereq']
        fac_id = json_data['faculty_id']
        course = Course.query.filter_by(course_id = cid).first()

        if course:
            perror("error")
            return redirect(url_for('add_course'))

        newcourse = Course(cid,cname,pre,fac_id)
        db.session.add(newcourse)
        db.session.commit()
        return redirect(url_for('faculty_home'), 302)


# API to approve a course
@app.route('/approve', methods = ['GET','POST'])
def approve():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            print("error")
            return redirect(url_for('approve'))
        cid = json_data['c_id']

        course = Course.query.filter_by(course_id = cid).first()

        if course:
            course.approve()
            return redirect(url_for('course_home'))
        else:
            perror("error")
            return redirect(url_for('error'))


# API to get list of all courses
@app.route('/allcourses')
def getAllCourses():
    j = Course.query.all()
    d = jsonify(json_data = [i.serialize for i in j])
    return d


# API to get list of all courses of a faculty
@app.route('/facultycourses')
def getFacultyCourses():
    return jsonify(json_data = [i.serialize for i in Course.query.filter_by(faculty = session['user_id']).all()])


# API to get all notices
@app.route('/allnotices')
def getAllNotices():
    for i in Notice.query.all():
        print i.serialize
    return jsonify(json_data = [i.serialize for i in Notice.query.all()])


# API to get all notices of a course
@app.route('/allcoursenotices')
def getCourseNotices():
    return jsonify(json_data = [i.serialize for i in Notice.query.filter_by(c_id = session['course_id']).all()])


# API to get all notices of a student
@app.route('/allstudentnotices')
def getStudentNotices():
    enrolled_courses = []
    for c in Enrolls.query.filter_by(student_id = session['user_id']).all():
        p = c.course_id
        enrolled_courses.append(p)

    d = jsonify(json_data = [i.serialize for i in Notice.query.all() if i.c_id in enrolled_courses])
    return d


# API for listing
@app.route('/listcourses', methods = ['GET'])
def list_course():
    return render_template('course_list.html')


# API for adding a lecture
@app.route('/addLecture', methods = ['GET' , 'POST'])
def addLecture():
    if request.method == 'POST' :
        json_data = result.get_json(force = True)
        # course_id = json_data['Course_Id']
        course_id = session['course_id']
        notes = json_data['Notes']
        Date_Time = json_data['Date_Time']
        Topic = json_data['Topic']
        Link = json_data['Link']
        # course_id = 1
        # notes = "abc"
        # Date_Time = "2012-12-12"
        # Topic = "topic"
        # link = "link"
        NewLec = Lecture(course_id, Date_Time, Topic)
        NewLec.setNotes(notes)
        NewLec.setLink(Link)
        db.session.add(NewLec)
        Lecture_Id= NewLec.Lecture_Id
        Questions = json_data['Questions']
        Answers = json_data['Answers']
        # Questions = "q"
        # Answers = "a"
        NewTest = Test(Lecture_Id, Questions, Answers)
        db.session.add(NewTest)
        db.session.commit()
        return redirect(url_for('course_home'))


if __name__ == "__main__":
    app.secret_key = "shubham12345"
    app.run(host="0.0.0.0", port = 5000, debug=True, threaded=True)
