from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from backend.auth import login
from . import db
from backend.models import User, Assignment, Entry, Announcement
from flask_login import login_required, current_user 
from flask import jsonify
from datetime import datetime
from datetime import date
from random import randint
import json

grade = Blueprint("grade", __name__)

@grade.route("/grade")
@login_required
def showGrades():
    return render_template("grade.html")


@grade.route("/getUngraded")
@login_required
def getUngraded():
    if request.method == "GET":

        # Start and end dates per semester 
        start_date = date(2021, 8, 30)
        end_date = date(2021, 12, 17)        

        ungraded = Assignment.query.join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.due_date<end_date, Entry.due_date>start_date).all()

        jsonArchive = []
        
        for item in ungraded:
            data = {}
            data["date"] = item.entry.complete_date
            data["name"] = item.assignment
            data["class"] = item.class_name
            data["id"] = item.id

            jsonArchive.append(data)
        
        return jsonify(jsonArchive)


    return render_template("grade.html")
