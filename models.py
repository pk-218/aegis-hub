from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    src_ip = db.Column(db.String(45))
    dest_ip = db.Column(db.String(45))
    src_port = db.Column(db.Integer)
    dest_port = db.Column(db.Integer)
    protocol = db.Column(db.Integer)
    size = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)