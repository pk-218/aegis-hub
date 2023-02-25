import sqlite3

def create_table():
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM Alerts;")
    conn.commit()
    conn.close()

create_table()