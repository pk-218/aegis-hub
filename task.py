import sqlite3

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