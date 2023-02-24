import sqlite3

# Connect to the database file
conn = sqlite3.connect('aegis.db')

# Create a cursor object
cur = conn.cursor()

# Define the SQL query
query = "SELECT * FROM Alerts;"

# Execute the query and fetch all results
cur.execute(query)
rows = cur.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the database connection
conn.close()