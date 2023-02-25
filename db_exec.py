import sqlite3
conn=sqlite3.connect('aegis.db')
cursor=conn.cursor()
# cursor.execute("INSERT INTO user (username, password) VALUES ('admin@gmail.com', 'password')")
# cursor.execute("CREATE TABLE User (username TEXT, password TEXT);")
# cursor.execute("DROP TABLE user")
conn.commit()
conn.close()