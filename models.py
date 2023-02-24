from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    src_ip = db.Column(db.String(45))
    dest_ip = db.Column(db.String(45))
    src_port = db.Column(db.Integer)
    dest_port = db.Column(db.Integer)
    protocol = db.Column(db.Integer)
    size = db.Column(db.Integer)

# class Packet(db.Model):
#     id: db.Column(db.Integer, primary_key=True, auto_increment=True)
#     src_ip: db.Column(db.String(45))
#     dest_ip: db.Column(db.String(45))
#     src_port: db.Column(db.Integer)
#     dest_port: db.Column(db.Integer)
#     protocol: db.Column(db.Integer)
#     size: db.Column(db.Integer)