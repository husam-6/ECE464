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


    # print(f"{assignment} has due date: {dueDate} with type: {classType}")
    # return render_template('edit.html')
    # request_method = request.method
    # if request.method == 'POST': 
    #     username = request.form['username']
    #     password = request.form['password']

    #     user = User.query.filter_by(username=username).first()

    #     if not user or not check_password_hash(user.password, password): 
    #         return redirect(url_for('auth.login'))

    #     login_user(user, remember=False)
    #     return redirect(url_for('main.planner'))
    # return render_template('auth.html', request_method = request_method)







    


