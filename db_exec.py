# from app import app, db
# from models import User

# # Push an application context
# with app.app_context():
#     # Create the table
#     db.create_all()

#     # Add a user
#     user = User(email='user@example.com', password='mypassword')
#     db.session.add(user)
#     db.session.commit()

import sqlite3
conn=sqlite3.connect('aegis.db')
cursor=conn.cursor()
# cursor.execute("INSERT INTO User (email, password) VALUES ('admin@gmail.com', 'password')")
# cursor.execute("CREATE TABLE User (email TEXT PRIMARY KEY, password TEXT);")
# cursor.execute("DROP TABLE user;")
conn.commit()
conn.close()
