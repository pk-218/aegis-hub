from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer)
    inode = db.Column(db.Integer)
    src_ip = db.Column(db.String(45))
    dst_ip = db.Column(db.String(45))
    protocol = db.Column(db.String(10))
    packet_size = db.Column(db.Integer)