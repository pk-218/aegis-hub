import sqlite3, alert, os
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fryyoudude@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

def insert_into_packet(json):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO Packet (id, process_id, inode, src_ip, dst_ip, protocol, packet_size) VALUES (?,?,?,?,?,?,?);", (json['id'],json['process_id'], json['inode'], json['src_ip'], json['dst_ip'], json['protocol'], json['packet_size']))
    conn.commit()
    conn.close()

def insert_into_alert(json):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO Alerts (datetime, threat, description) VALUES ('{datetime.now()}','Malicious IP detected','Your device has contacted a possibly malicious IP: {json['src_ip']}')")
    conn.commit()
    conn.close()

def processor(json):
    malicious_ip_rule(json)

def malicious_ip_rule(json):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM malicious_ip WHERE ip = '{json['src_ip']}'")
    result = c.fetchone()
    if result is not None:
        print("HEREEEE")
        try:
            alert.send_mail_alert_alternative(
                subject="Possibly Malicious IP Hit Detected",
                sender='fryyoudude@gmail.com',
                recipients=['thakareprasad80@gmail.com'],
                body="We have detected a malicious IP hit on your device"
            )
        except Exception as e:
            print("An error occurred:", e)
    conn.commit()
    conn.close()