from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    request_method = request.method
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('auth.mainReturn', username = username))
    return render_template('auth.html', request_method = request_method)

@auth.route('/planner/<string:username>', methods=['GET', 'POST'])
def mainReturn(username):
    return render_template('index.html')
