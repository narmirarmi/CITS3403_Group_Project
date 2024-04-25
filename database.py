import sqlite3

DB_FILE = r'database\database.db'

"""
    # Example SELECT query
    query_database("SELECT * FROM Users;")

    # Example INSERT query
    query_database("INSERT INTO Users (Username, Email, Password) VALUES ('user1', 'user1@example.com', 'password1');")

    # Example UPDATE query
    query_database("UPDATE Users SET Password = 'newpassword' WHERE UserID = 1;")

    # Example DELETE query
    query_database("DELETE FROM Users WHERE UserID = 2;")
"""

def create_database_from_sql(sql_file):
    with open(sql_file, 'r') as file:
        sql_commands = file.read()

    # Connect to the SQLite database (if the database doesn't exist, it will be created)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Execute SQL commands
    cursor.executescript(sql_commands)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def query_database(query):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Execute the SQL query
        cursor.execute(query)

        # Fetch the results (if needed)
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row)

        # Commit changes for INSERT, UPDATE, DELETE queries
        if query.strip().lower().startswith(('insert', 'update', 'delete')):
            conn.commit()

    except sqlite3.Error as e:
        print("Error executing query:", e)

    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()

