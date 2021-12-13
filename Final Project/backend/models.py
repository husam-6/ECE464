from . import db
from flask_login import UserMixin
from sqlalchemy.orm import backref

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # uid
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gpa = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.username

class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key= True, nullable=False) # aid
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    viewType = db.Column(db.Boolean, nullable=False)
    complete_date = db.Column(db.DateTime, nullable=True)

    #one to many (one user to many entries)
    user = db.relationship("User", backref="Entry", lazy=True)

class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    announcement = db.Column(db.String(80), nullable=False)
    # description = db.Column(db.String(300), nullable=False)

    #one to one relationship (one entry to one announcement)
    entry = db.relationship('Entry', uselist=False, backref="Announcement")

class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable = False)
    assignment = db.Column(db.String(80), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    a_type = db.Column(db.String(20), nullable=False)

    # one assignment to many grades
    grades = db.relationship("Grade", backref="Assignment", lazy=True, uselist=True)

    #one to one relationship (one entry to one assignment)
    entry = db.relationship('Entry', uselist=False, backref="Assignment")

    #One to many relationships (One entry to many notifications)
    notif = db.relationship('Notification', uselist=True)

class Grade(db.Model):
    __tablename__ = "grade"
    id = db.Column(db.Integer, primary_key=True, nullable=False) # gid
    grade = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)

    #one to one relationship (one grade to one user)
    # assignment = db.relationship("Assignment", single_parent = True, backref="Grade", cascade="all, delete, delete-orphan", lazy=True, uselist=False)
    
    #One to many relationship (one user to many grades)
    user = db.relationship("User", backref="Grade", lazy=True, uselist=True)

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    notif_date = db.Column(db.DateTime, nullable=False)

class Snooze(db.Model): 
    __tablename__ = 'snooze'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(80))
    classname = db.Column(db.String(80))
    snooze_time = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String(80))
