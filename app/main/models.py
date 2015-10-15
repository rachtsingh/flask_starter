#!/usr/bin/env python
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Example(db.Model):
    __tablename__ = "example"
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
		pass

    def __repr__(self):
        return '<Example {}>'.format(self.id)

