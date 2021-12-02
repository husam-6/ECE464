from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from . import db

main = Blueprint("main", __name__)

@main.route('/')
def root(): 
    return redirect(url_for('auth.login'))

class User(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gpa = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.username


# @app.route('/')
# def hello_negro():
#     return "Hello Negro!!!!"
# @app.route('/')


if __name__ == '__main__':
    main.run(debug=True)
