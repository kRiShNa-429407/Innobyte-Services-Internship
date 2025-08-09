## Create the Database and users Table
import sqlite3

def initialize_database():
    """
    Initializes the database and creates the necessary tables
    if they don't already exist.
    """

    # connect() will create 'finance.db' file if it doesn't exist
    db = sqlite3.connect('finance.db')

    # A cursor is used to execute SQL commands
    cursor = db.cursor()

    # Create the 'users' table.
    # 'IF NOT EXISTS' prevents an error if the table is already there.
    #  # 'IF NOT EXISTS' prevents an error if the table is already there.
    # 'id INTEGER PRIMARY KEY' creates an auto-incrementing ID for each user.
    # 'username TEXT UNIQUE NOT NULL' ensures every username is unique and not empty.

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   username TEXT UNIQUE NOT NULL,
                   password_hash TEXT NOT NULL)

                   ''')
    
    # Add this new table for transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL, -- 'income' or 'expense'
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    print("Database initialized and 'users' table is ready.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        limit_amount REAL NOT NULL,
        UNIQUE(user_id, category),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

    # Commit the changes and close the connection
    db.commit()
    db.close()


