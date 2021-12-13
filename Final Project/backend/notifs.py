from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from backend.models import Assignment, Entry, Grade
from flask_login import login_required, current_user 
from flask import jsonify
from flask_mail import Mail, Message
from backend.models import Notification, Snooze
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import date
from .generate import generateID

notifs = Blueprint("notifs", __name__)

@notifs.route("/notification")
@login_required
def notifMain():
    return render_template("notifs.html")
     


@notifs.route("/notifs", methods=['GET', 'POST'])
@login_required
def notifications():
    if request.method == "POST":
        message = request.form['message']
        date = request.form['reminder']
        email = request.form['email']
        classname = request.form['class']
        snoozeDate = datetime.strptime(date,"%Y-%m-%d")
    

        sid = generateID(Snooze)
        snooze = Snooze(id=sid, email=email, classname=classname, description=message, snooze_time=snoozeDate)
        
        db.session.add(snooze)
        db.session.commit()
    # today = datetime.date(2021,11,28)
    # notifs = Notification.query.first()
    
    # tmp = str(notifs.notif_date)
    # tmp = tmp[:10]
    # print(tmp, today)
    # if tmp == str(today):
    #     print("MASSIVE COCK")

    return redirect(url_for("notifs.notifMain"))

@notifs.route("/notification/display", methods=["GET", "POST"])
@login_required
def displayNotifs():
    return render_template("showNotifs.html")

@notifs.route('/getNotifs', methods = ['GET', 'POST'])
@login_required
def getNotifs():
    if request.method == "POST":
        startDate = request.form['start-date']
        endDate = request.form['end-date']        
        
        notifs = db.session.query(Notification, Assignment).join(Notification, Notification.assignment_id == Assignment.id).filter(Notification.notif_date>startDate, Notification.notif_date<endDate).all()

        snooze = Snooze.query.filter(Snooze.snooze_time<endDate, Snooze.snooze_time>startDate).all()


        notifJSON = []
        snoozeJSON = []

        for item in notifs:
            data = {}
            data["id"] = item[0].id
            data["date"] = item[0].notif_date
            data["name"] = item[1].assignment
            data["color"] = item[1].a_type
            data["class"] = item[1].class_name

            notifJSON.append(data)
        
        for item in snooze: 
            data = {}
            data["id"] = item.id
            data["date"] = item.snooze_time
            data["desc"] = item.description
            data["class"] = item.classname

            snoozeJSON.append(data)

        # print(notifJSON, snoozeJSON)
        
        return render_template("notifsFiltered.html", notifJSON=notifJSON, snoozeJSON=snoozeJSON)
        
    if request.method == "GET":

        pendingNotifs = db.session.query(Notification, Assignment).join(Notification, Notification.assignment_id == Assignment.id).all()
        pendingSnooze = Snooze.query.all()
        
        notifsJSON = []
        # print(pendingNotifs)
        
        for item in pendingNotifs:
            data = {}
            data["date"] = item[0].notif_date
            data["name"] = item[1].assignment
            data["color"] = item[1].a_type
            data["class"] = item[1].class_name
            data["id"] = item[0].id

            notifsJSON.append(data)
        
        return jsonify(notifsJSON)

@notifs.route('/getNotifs/snooze', methods = ['GET', 'POST'])
@login_required
def getSnoozes():
    if request.method == "GET":

        pendingSnooze = Snooze.query.all()
        
        notifsJSON = []
        # print(pendingNotifs)
        
        for item in pendingSnooze:
            data = {}
            data["date"] = item.snooze_time
            data["desc"] = item.description
            data["class"] = item.classname
            data["id"] = item.id

            notifsJSON.append(data)
        
        return jsonify(notifsJSON)


#I think this works now
from backend import create_app
app = create_app()
app.app_context().push()
def scheduled_job():
    with app.app_context():
        today = datetime.now()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0) 


        snoozes = Snooze.query.filter(Snooze.snooze_time==today).all()
        
        notifs = db.session.query(Notification, Assignment).join(Notification, Notification.assignment_id == Assignment.id).filter(Notification.notif_date==today).all()

        snoozes = Snooze.query.filter(Snooze.snooze_time==today).all()
        
        # print(notifs)
        # print(snoozes)

        mail = Mail(current_app)
        
        for item in notifs: 
            msg = Message(item[1].class_name, sender='lurdytad@gmail.com', recipients=['ladturdy@gmail.com', 'husam.almanakly@cooper.edu', 'layth.yassin@cooper.edu'])
            msg.body = "Reminder! 3 Days left for " + item[1].assignment
            mail.send(msg)

        for item in snoozes: 
            msg = Message(snoozes.classname, sender='lurdytad@gmail.com', recipients=['ladturdy@gmail.com', 'husam.almanakly@cooper.edu', 'layth.yassin@cooper.edu'])
            msg.body = item.description
            mail.send(msg)
        # msg = Message("Hello", sender='lurdytad@gmail.com', recipients=['husam.almanakly@cooper.edu'])
        # msg.body = "Test"
        # mail.send(msg)


# sched.start()

sched = BackgroundScheduler(daemon=True, timezone="EST")
# sched.add_job(scheduled_job,'interval',seconds=10)
sched.add_job(scheduled_job,'cron',day_of_week="mon-sun", hour = "8")
sched.start()

