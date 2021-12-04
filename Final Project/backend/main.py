from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from backend.models import User, Assignment, Entry, Announcement
from flask_login import login_required, current_user 
from flask import jsonify
from datetime import datetime
from datetime import date
from random import randint
import json

main = Blueprint("main", __name__)

@main.route('/')
def root(): 
    # ali = User(id = 1, username="aghuman", password=generate_password_hash("123suckad", method="sha256"), email="ali.ghuman@cooper.edu", gpa=3.84)
    # husam = User(id=2, username="halmanakly", password=generate_password_hash("yaryar123", method="sha256"), email="husam.almanakly@cooper.edu", gpa=3.92)
    # layth = User(id=3, username="lyassin", password=generate_password_hash("smallcock69", method="sha256"), email="layth.yassin@cooper.edu", gpa=3.9)

    # # with app.app_context():
    # db.session.add(ali)
    # db.session.add(husam)
    # db.session.add(layth)
    # db.session.commit()
    return redirect(url_for('auth.login'))

# @main.route('/planner')
# @login_required
# def planner():
#     return render_template('index.html')


@main.route('/planner', methods=["GET", "POST"])
@login_required
def planner():
    def generateID(Table):
        tid = randint(1, 2**32)
        tmp = Table.query.filter_by(id=tid).first()
        while tmp:
            tid = randint(1, 2**32)
            tmp = Table.query.filter_by(id=tid).first()
            
        return tid
    if request.method == "POST":
        form_name = request.form['submit_btn']
        if form_name == 'p_submit':
            dueDate = datetime.strptime(request.form['due_date'],"%Y-%m-%d")
            className = request.form['class_name']
            assignment = request.form['assignment']
            classType = request.form['class_type']
            
            eid = generateID(Entry)
            entry = Entry(id=eid, user_id=current_user.id, due_date=dueDate, viewType=True)
            entry.user = current_user
            
            aid = generateID(Assignment)
            item = Assignment(id=aid, entry_id=entry.id, assignment=assignment, class_name=className, a_type=classType, entry=entry)
            item.entry = entry
            

            db.session.add(item)
            db.session.commit()
            # print(f"{assignment} has due date: {dueDate} with type: {classType}")
            return redirect(url_for('main.planner'))
        
        elif form_name == 'a_submit':
            dueDate = datetime.strptime(request.form['announce-date'],"%Y-%m-%d")
            announcement = request.form['announcement']

            eid = generateID(Entry)
            entry = Entry(id=eid, user_id=current_user.id, due_date=dueDate, viewType=False)
            entry.user = current_user
            
            aid = generateID(Assignment)
            item = Announcement(id=aid, entry_id=entry.id , announcement=announcement)
            item.entry = entry
            
            db.session.add(item)
            db.session.commit()

            return redirect(url_for('main.planner'))
        
    return render_template('index.html')

@main.route('/getEntries', methods=["GET"])
def getEntries():
    entries = Assignment.query.join(Entry).filter(Entry.complete_date==None).all()
    # entries = Assignment.query.filter(Assignment.entry.complete_date==None).all()
    # print(entries)

    items = []
    
    for item in entries:
        data = {}
        data["date"] = item.entry.due_date
        data["name"] = item.assignment
        data["completed"] = item.entry.complete_date
        data["color"] = item.a_type
        data["class"] = item.class_name
        data["id"] = item.id

        items.append(data)
    
    return jsonify(items)

@main.route('/announce', methods=["GET"])
def announcementEntries():
    entries = Announcement.query.join(Entry).filter(Entry.complete_date==None, Entry.user_id==current_user.id, Entry.viewType==False).all()

    # print(entries)

    items = []
    
    for item in entries:
        data = {}
        data["date"] = item.entry.due_date
        data["name"] = item.announcement
        data["completed"] = item.entry.complete_date
        data["id"] = item.id

        items.append(data)
    
    return jsonify(items)


@main.route('/delete', methods=["POST"])
def delItem():
    delId = json.loads(request.data)
    print("UNBELIEVABLY HUGE PEEEEENIS!!!!!!!!!!!!!!!!!!")
    form_name = request.form["sub-btn"]
    
    if form_name == "announceItem":
        tmp = Announcement.query.filter(Announcement.id == delId['value']).first()
    elif form_name == "planItem":
        tmp = Assignment.query.filter(Assignment.id == delId['value']).first()
    
    tmp.entry.complete_date = date.today()
    db.session.commit()

    return delId

@main.route('/calendar', methods=["GET"])
def allItems():
    calItems = Assignment.query.join(Entry).with_entities(Entry.due_date, Assignment.assignment, Entry.complete_date, Assignment.a_type, Assignment.class_name, Assignment.id).all()
    
    items = []
    
    for item in calItems:
        data = {}
        data["date"] = item[0]
        data["name"] = item[1]
        data["completed"] = item[2]
        data["color"] = item[3]
        data["class"] = item[4]
        data["id"] = item[5]

        items.append(data)
    
    return jsonify(items)

if __name__ == '__main__':
    main.run(debug=True)
