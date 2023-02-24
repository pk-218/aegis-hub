from flask import Flask
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

from models import db, Packet

db.init_app(app)

@app.route("/add-entry")
def home():
    with app.app_context():
        packet = Packet(process_id=1234, inode=5678, src_ip='192.168.1.1', dst_ip='192.168.1.2', protocol='tcp', packet_size=100)
        db.session.add(packet)
        db.session.commit()
    # new_packet = Packet(process_id=1234, inode=5678, src_ip='192.168.0.1', dst_ip='192.168.0.2', protocol='TCP', packet_size=1500)
    # db.session.add(new_packet)
    # db.session.commit()
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

@app.route("/sms-alert")
def sms():
    alert.send_sms_alert(
        title="Hello",
        desc="Hello!"
    )

    return "Hello"

if __name__ == "__main__":
    app.run(debug=True, port=8000)

# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     if request.method=='POST':
#         title = request.form['title']
#         desc = request.form['desc']
#         alert.send_sms_alert(title, desc)
#         todo = Todo(title=title, desc=desc)
#         db.session.add(todo)
#         db.session.commit()
        
#     allTodo = Todo.query.all() 
#     return render_template('index.html', allTodo=allTodo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
