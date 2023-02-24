from datetime import datetime
import sqlite3
c = sqlite3.connect('aegis.db')
cursor=c.cursor()
cursor.execute("ALTER TABLE Alerts DROP PRIMARY KEY;")
c.commit()
c.close()
