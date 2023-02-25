from flask import Flask, render_template, flash, redirect, request, session, url_for
from flask_mailman import Mail
import os
import middleware
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aegis.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fryyoudude@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['SECRET_KEY'] = 'thisismysecret'

from auth import auth_bp

app.register_blueprint(auth_bp)

db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)


@app.route('/')
def home2():
    if(session['logged_in']):
        return render_template('index.html')
    else:
        return redirect(url_for('auth_bp.login'))

@app.route('/create_table', methods=['GET'])
def home():
    middleware.create_table()
    middleware.insert_into_malicious_ip()
    alerts = middleware.get_all_alerts()
    return render_template('index.html', alerts=alerts)

@app.route("/process-logs", methods = ['POST'])
def processor(): 
    data = request.get_json()
    print(int(data["time"][21:28]))
    middleware.insert_into_packet_2(data)
    middleware.processor(data)
    return "HELLO"

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True, port=8000)

