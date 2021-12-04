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
            # print(request.form['pubpriv'])
            try:
                view = request.form['pubpriv']
                if view == "on":
                    view = False
            except:
                view = True
            
            # print(view)
            # view = True
            eid = generateID(Entry)
            entry = Entry(id=eid, user_id=current_user.id, due_date=dueDate, viewType=view)
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
@login_required
def getEntries():
    entries = Assignment.query.join(Entry).filter(((Entry.complete_date==None) & (Entry.viewType==True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date==None))).all()
    # entries = Assignment.query.join(Entry).filter((Entry.complete_date==None) | ((Entry.user_id == current_user.id) & (Entry.viewType==True))).all()
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
@login_required
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
@login_required
def delItem():
    delId = json.loads(request.data)
    
    form_name = delId['type']
    
    if form_name == "announceItem":
        tmp = Announcement.query.filter(Announcement.id == delId['value']).first()
    elif form_name == "planItem":
        tmp = Assignment.query.filter(Assignment.id == delId['value']).first()
    
    tmp.entry.complete_date = date.today()
    db.session.commit()

    return delId

@main.route('/calendar', methods=["GET"])
@login_required
def allItems():
    calItems = Assignment.query.join(Entry).all()
    

    items = []
    
    for item in calItems:
        data = {}
        data["date"] = item.entry.due_date
        data["name"] = item.assignment
        data["completed"] = item.entry.complete_date
        data["color"] = item.a_type
        data["class"] = item.class_name
        data["id"] = item.id

        items.append(data)
    
    return jsonify(items)

@main.route('/edit&id=<int:id>', methods=["GET", "POST"])
@login_required
def editItem(id):
    if request.method == "POST":
        dueDate = datetime.strptime(request.form['due_date'],"%Y-%m-%d")
        className = request.form['class_name']
        assignment = request.form['assignment']
        classType = request.form['class_type']
        # aid = request.form["id"]
        aid=id

        item = Assignment.query.filter(Assignment.id == aid).first()

        item.entry.due_date = dueDate
        item.assignment = assignment
        item.a_type = classType
        item.class_name = className

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.planner'))

    # print(f"{assignment} has due date: {dueDate} with type: {classType}")
    return render_template('edit.html')

if __name__ == '__main__':
    main.run(debug=True)
