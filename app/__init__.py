#!/usr/bin/env python
import os
import traceback
from flask import Flask, Blueprint, request, render_template, g, session, redirect, url_for, make_response

# import Flask extensions
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy(app)

from main.controllers import main as main_module
app.register_blueprint(main_module)

app.secret_key = "sajfdasf1389flj1u34ljsdfldksalf1231e89sfdshfk"

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.route('/', methods=['GET'])
def index():
	return render_template('index/index.html')

