from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import alert
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aegis.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fryyoudude@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)

class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer)
    inode = db.Column(db.Integer)
    src_ip = db.Column(db.String(45))
    dst_ip = db.Column(db.String(45))
    protocol = db.Column(db.String(10))
    packet_size = db.Column(db.Integer)

@app.route("/add-entry")
def home():
    # db.session.execute('SHOW tables;')
    new_packet = Packet(process_id=1234, inode=5678, src_ip='192.168.0.1', dst_ip='192.168.0.2', protocol='TCP', packet_size=1500)
    db.session.add(new_packet)
    db.session.commit()
    return "Hello"

@app.route("/mail")
def mail():
    alert.send_mail_alert(
        app,
        subject='You have been hacked!',
        sender='noreply@demo.com',
        recipients=['ama_b19@ce.vjti.ac.in'],
        body='Your rasberry PI has been compromised'
    )
    return "mail sent"

if __name__ == "__main__":
    app.run(debug=True, port=8000)






