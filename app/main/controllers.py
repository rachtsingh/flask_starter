#!/usr/bin/env python
import os
import traceback
from flask import Flask, Blueprint, request, render_template, g, session, redirect, url_for, make_response

main = Blueprint('main', __name__)

@main.route('/main')
def main_func():
	return 42

