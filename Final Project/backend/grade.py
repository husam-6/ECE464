from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from backend.auth import login
from . import db
from backend.models import Assignment, Entry, Grade
from flask_login import login_required, current_user 
from flask import jsonify
from datetime import datetime
from datetime import date
from random import randint
from .generate import generateID

grade = Blueprint("grade", __name__)

@grade.route("/grade", methods=['GET', 'POST'])
@login_required
def showGrades():
    return render_template("grade.html")


@grade.route("/getGrades", methods=['GET', 'POST'])
@login_required
def getUngraded():
    if request.method == "GET":

        # Start and end dates per semester 
        start_date = date(2021, 8, 30)
        end_date = date(2021, 12, 17)        

        ungraded = Assignment.query.join(Entry).join(Grade, Grade.assignment_id == Assignment.id).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<end_date, Entry.complete_date>start_date).filter((Grade.user_id != current_user.id)).all()

        graded = Assignment.query.join(Grade, Grade.assignment_id == Assignment.id).filter(Grade.user_id==current_user.id).all()

        for item in graded: 
            if item in ungraded: 
                ungraded.remove(item)
         
        # ungraded2 = Assignment.query.join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<end_date, Entry.complete_date>start_date).all()
        
        tmp = db.session.query(Assignment, Grade).outerjoin(Grade, Assignment.id == Grade.assignment_id).join(Entry).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<end_date, Entry.complete_date>start_date).all()
        
        ungraded2 = []
        for item in tmp:
            if item[1] == None:
               ungraded2.append(item[0]) 
        
        # print(ungraded2)
        ungraded+=ungraded2
        # print(ungraded)

        jsonArchive = []
        
        for item in ungraded:
            data = {}
            data["completed"] = item.entry.complete_date
            data["name"] = item.assignment
            data["class"] = item.class_name
            data["id"] = item.id
            data["color"] = item.a_type

            jsonArchive.append(data)
        
        return jsonify(jsonArchive)
    return render_template("grade.html")

@grade.route("/gradedItems", methods=['GET', 'POST'])
@login_required
def getGraded():
    if request.method == "GET":

        # Start and end dates per semester 
        start_date = date(2021, 8, 30)
        end_date = date(2021, 12, 31)        

        # ungraded = Assignment.query.join(Entry).join(Grade).filter(((Entry.complete_date != None) & (Entry.viewType == True)) | ((Entry.user_id == current_user.id) & (Entry.complete_date != None))).filter(Entry.complete_date<end_date, Entry.complete_date>start_date).filter(Assignment.grade != None).all()
        
        graded = Grade.query.filter(Grade.user_id==current_user.id).all()
        
        jsonArchive = []
        
        for item in graded:
            data = {}
            tmp = Assignment.query.filter(Assignment.id == item.assignment_id).first()
            
            data["completed"] = tmp.entry.complete_date
            data["name"] = tmp.assignment
            data["class"] = tmp.class_name
            data["id"] = item.id
            data["color"] = tmp.a_type
            data["grade"] = item.grade
            data["weight"] = item.weight

            jsonArchive.append(data)
        
        return jsonify(jsonArchive)



@grade.route("/insert_grade&id=<int:id>", methods=["GET", "POST"])
@login_required
def insertGrade(id):
    if request.method == "POST":
        grade = float(request.form['grade'])
        weight = float(request.form['weight'])
        
        # print(grade, weight, "PENISSSSS")
        # aid = request.form["id"]
        aid=id

        item = Assignment.query.filter(Assignment.id == aid).first()
        gid = generateID(Grade)
        gradeItem = Grade(id=gid, grade=grade, weight=weight, user_id=current_user.id, assignment_id=item.id)

        item.grades.append(gradeItem)
        
        db.session.add(gradeItem)
        db.session.commit()
        
        return redirect(url_for('grade.showGrades'))

    # print(f"{assignment} has due date: {dueDate} with type: {classType}")
    return render_template('grade.html')

@grade.route("/editGrade&id=<int:id>", methods=["GET", "POST"])
@login_required
def editGrade(id):
    if request.method == "POST":
        newGrade = float(request.form['grade'])
        newWeight = float(request.form["weight"])
        print(newGrade, newWeight)

        item = Grade.query.filter(Grade.id == id).first()

        item.grade = newGrade
        item.weight = newWeight

        db.session.commit()

        return redirect(url_for('grade.showGrades'))

    return render_template("editGrade.html")

@grade.route("/getGPA", methods=["GET", "POST"])
@login_required
def getGPA(): 
    if request.method == "GET":
        
        classes = db.session.query(Assignment.class_name, db.func.sum(Grade.weight*Grade.grade), db.func.sum(Grade.weight)).join(Assignment, Assignment.id == Grade.assignment_id).filter(Grade.user_id==current_user.id).group_by(Assignment.class_name).all()

        jsonArchive = []

        for item in classes:
            data = {}
            
            data["class"] = item[0]
            data["grade"] = item[1]/item[2]

            jsonArchive.append(data)
        
        return jsonify(jsonArchive)

    


@grade.route("/gpa", methods=["GET", "POST"])
@login_required
def gpa():
    return render_template("gpa.html")