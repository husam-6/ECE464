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
from datetime import datetime
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


# sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=8)
# def scheduled_job():
#     today = datetime.date.today()
#     notifs = Notification.query.filter((Notification.notif_date==today) | (Notification.snooze_time==today)).all()
    
#     tmp = str(notifs.notif_date)
#     tmp = tmp[:10]
#     # print(tmp, today)
#     mail = Mail(current_app)
    
#     for item in notifs: 
#         if tmp == str(today):
#             msg = Message(notifs.classname, sender='lurdytad@gmail.com', recipients=['ladturdy@gmail.com', 'husam.almanakly@cooper.edu', 'xueru.zhou@cooper.edu', 'layth.yassin@cooper.edu'])
#             msg.body = item.description
#             mail.send(msg)
#             # print("MASSIVE COCK")


# sched.start()
