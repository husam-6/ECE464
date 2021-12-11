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

arch = Blueprint("arch", __name__)

@arch.route('/arch', methods = ['GET', 'POST'])
@login_required
def archive():
    return render_template("arch.html")


@arch.route('/getArch', methods = ['GET', 'POST'])
@login_required
def getArchive():
    if request.method == "POST":
        startDate = request.form['start-date']
        endDate = request.form['end-date']
        className = request.form['class_name']
        
        try:
            classType = request.form['class_type']
            archived = Assignment.query.join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<endDate, Entry.complete_date>startDate, Assignment.class_name == className, Assignment.a_type == classType).all()
        except: 
            # print("TEST")
            archived = Assignment.query.join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<endDate, Entry.complete_date>startDate, Assignment.class_name == className).all()

        retJSON = []

        for item in archived:
            data = {}
            data["date"] = item.entry.due_date
            data["name"] = item.assignment
            data["completed"] = item.entry.complete_date
            data["color"] = item.a_type
            data["class"] = item.class_name
            data["id"] = item.id

            retJSON.append(data)
        
        # tmp = jsonify(retJSON)
        tmp = retJSON
        # print(tmp)
        return render_template("filtered.html", tmp=tmp)

    if request.method == "GET":
        archived = Assignment.query.join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).all()

        jsonArchive = []
        
        for item in archived:
            data = {}
            data["date"] = item.entry.due_date
            data["name"] = item.assignment
            data["completed"] = item.entry.complete_date
            data["color"] = item.a_type
            data["class"] = item.class_name
            data["id"] = item.id

            jsonArchive.append(data)
        
        return jsonify(jsonArchive)

@arch.route('/arch&id=<int:id>', methods=["GET"])
@login_required
def recover(id):
    print(id)
    if request.method == "GET":
        aid = id
        item = Assignment.query.filter(Assignment.id == aid).first()

        item.entry.complete_date = None

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('arch.archive'))
    
    return render_template('arch.html')
