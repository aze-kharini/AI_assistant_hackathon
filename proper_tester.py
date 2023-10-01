import sqlite3

database_file = '/home/viridis/VSCode/CK401/AI_dev/jupyter_db.db' # this is where you need to put in the absolute path to the db


def connect_fun(database_name):
    try:
        connection = sqlite3.connect(database_file)
        print("Connected to the database")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Connect to the SQLite database
conn = connect_fun(database_file)
cursor = conn.cursor()
# Fetch the schema information
cursor.execute("SELECT * FROM sqlite_master;")
table_master = cursor.fetchall()

for row in table_master:
    print(row)
