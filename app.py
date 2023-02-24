from flask import Flask, request, render_template, session, redirect, url_for
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

from models import db, Packet, User

db.init_app(app)

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)



# @app.route('/login-render', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return render_template('index.html')
        u = request.form['username']
        p = request.form['password']
        print(u, p)
        data = User.query.filter_by(username=u, password=p).first()
        print(data)
        if data is not None:
            print('logged in')
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/action-center', methods=['GET','POST'])
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

