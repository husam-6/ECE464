from flask import Flask
from __init__ import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SQLALCHEYMY_DATABASE_URI'] = 'sqlite:///test.db'
# db.init_app(app)

ali = User(uid = 1, username="aghuman", password=generate_password_hash("123suckad", method="sha256"), email="ali.ghuman@cooper.edu", gpa=3.84)
husam = User(uid=2, username="halmanakly", password=generate_password_hash("yaryar123", method="sha256"), email="husam.almanakly@cooper.edu", gpa=3.92)
layth = User(uid=3, username="lyassin", password=generate_password_hash("smallcock69", method="sha256"), email="layth.yassin@cooper.edu", gpa=3.9)

# with app.app_context():
db.session.add(ali)
db.session.add(husam)
db.session.add(layth)
db.session.commit()
