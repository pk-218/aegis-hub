from flask import Flask, request, render_template
import os
import json
import middleware

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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/process-logs", methods = ['POST'])
def processor(): 
    data = json.loads(request.get_json()) # data is python dictionary
    middleware.insert_into_packet(data)
    middleware.processor(data)
    return "HELLO"

if __name__ == "__main__":
    app.run(debug=True, port=8000)

