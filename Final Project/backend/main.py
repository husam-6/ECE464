from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from backend.models import User
from flask_login import login_required, current_user 

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

@main.route('/planner')
@login_required
def planner():
    return render_template('index.html')

if __name__ == '__main__':
    main.run(debug=True)
