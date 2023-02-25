import sqlite3, alert, os
from datetime import datetime
from flask import Flask
import time

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fryyoudude@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

print("Wow!")

def create_table():
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"CREATE TABLE Packet1(id int PRIMARY_KEY AUTO_INCREMENT, src_ip text, dest_ip text, src_port int, dest_port int, protocol int,size int, timestamp int);")
    conn.commit()
    # conn.close()

    c.execute(f"CREATE TABLE Malicious_ip(ip text);")
    conn.commit()
    # conn.close()

    c.execute(f"CREATE TABLE Alerts(datetime text, threat, description);")
    conn.commit()
    conn.close()

def insert_into_packet_2(json):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO Packet1 (src_ip, dest_ip, src_port, dest_port, protocol, size, timestamp) VALUES (?,?,?,?,?,?,?);", (json["src_ip"], json["dest_ip"], json["src_port"], json["dest_port"], json["protocol"], json["size"], int(time.time())))
    conn.commit()
    conn.close()


def insert_into_malicious_ip():
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO Malicious_ip (ip) VALUES ('1.1.1.1');")
    conn.commit()
    conn.close()


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
    detect_dos_attack(json)
    detect_udp_flood(json)
    packet_length()


def get_all_alerts():
    conn = sqlite3.connect('aegis.db')
    cur = conn.cursor()
    query = "SELECT * FROM Alerts;"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

#rules
def malicious_ip_rule(json):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM malicious_ip WHERE ip = '{json['src_ip']}'")
    result = c.fetchone()
    if result is not None:
        print("HEREEEE")
        try:
            c.execute(f"INSERT into Alerts values('{datetime.now()}', 'Malicious IP', 'The IP was malicious!')")
            conn.commit()
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


def detect_dos_attack(json):
    # establish a connection to your database
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()

    ip_address = json['src_ip']
    
    # create a cursor object to execute SQL queries
    # cursor = db.cursor()
    
    # execute the SQL query to count the number of requests from the given IP address in the last 5 minutes
    query = "SELECT COUNT(*) AS num_requests FROM Packet1 WHERE src_ip = ? AND timestamp BETWEEN strftime('%s', 'now', '-5 minutes') AND strftime('%s', 'now')"
    c.execute(query, (ip_address,))
    
    # fetch the query results
    result = c.fetchone()
    # print(result[0])
    
    # close the database connection and cursor
    # cursor.close()
    # db.close()
    
    # determine if the number of requests is above a certain threshold (e.g., 100)
    if result[0] > 500:
        print("Oh nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            c.execute(f"INSERT into Alerts values('{datetime.now()}', 'DoS', 'There were too many requests from a particular IP!')")
            conn.commit()
            # alert.send_mail_alert_alternative(
            #     subject="Brute Force attack!!",
            #     sender='fryyoudude@gmail.com',
            #     recipients=['thakareprasad80@gmail.com'],
            #     body="Someone is trying to flood your server with multiple requests"
            # )
        except Exception as e:
            print("An error occurred:", e)
    conn.close()


def detect_udp_flood(json):
    # Connect to the database
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()

    ip_address = json['src_ip']

    # Query the database to get the number of UDP packets and the total packet size received from the IP address in the last 5 minutes
    query = f"SELECT COUNT(*), SUM(size) FROM Packet1 WHERE dest_ip = '{ip_address}' AND protocol = 'UDP' AND timestamp BETWEEN strftime('%s', 'now', '-5 minutes') AND strftime('%s', 'now')"
    c.execute(query)
    num_udp_packets, total_packet_size = c.fetchone()
    print(num_udp_packets)
    # Close the database connection
    

    if type(num_udp_packets) == int and type(total_packet_size) == int:
    # Check if the number of UDP packets received or the total packet size is above the threshold for a UDP flood attack
        if (num_udp_packets > 100 or total_packet_size > 1048576): # 1 MB in bytes
            print("Oh nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            try:
                c.execute(f"INSERT into Alerts values('{datetime.now()}', 'UDP Flooding', 'UDP Flooding!')")
                conn.commit()
                # alert.send_mail_alert_alternative(
                #     subject="Brute Force attack!!",
                #     sender='fryyoudude@gmail.com',
                #     recipients=['thakareprasad80@gmail.com'],
                #     body="Someone is trying to flood your server with multiple requests"
                # )
            except Exception as e:
                print("An error occurred:", e)

        else:
            print("lol")
        conn.close()


    

def packet_length():
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    query = f"SELECT SUM(size), dest_ip from Packet1 group by dest_ip;"
    c.execute(query)
    res = c.fetchall()
    print(res)
    for i in res:
        c.execute(f"select * from alerts where threat='Packet Length Exceeding';")
        alerts = c.fetchall()        
        if i[0]>10000*10000:
            print("ALERT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            c.execute(f"INSERT INTO Alerts (datetime, threat, description) values('{str(datetime.now())}', 'Packet Length Exceeding', 'Device is getting too many requests from a single IP {i[1]} for a long time');")
            conn.commit()
            for alert in alerts:
                if i[1] not in alert:
                    print("ALERT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    c.execute(f"INSERT INTO Alerts (datetime, threat, description) values('{str(datetime.now())}', 'Packet Length Exceeding', 'Device is getting too many requests from a single IP {i[1]} for a long time');")
                    conn.commit()
    conn.close()