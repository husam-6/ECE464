from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    request_method = request.method
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password): 
            return redirect(url_for('auth.login'))

        login_user(user, remember=False)
        return redirect(url_for('main.planner'))
    return render_template('auth.html', request_method = request_method)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))