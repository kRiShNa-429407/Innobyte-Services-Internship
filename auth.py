## This file will handle user's registration and login.

import sqlite3  # to work with database
import hashlib  # secure password , it's like encoding

def hash_password(password):
    """
    Hashes a password for secure storage.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# Register user function
def register_user(username , password):
    """Register a new user in the database."""
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username , password_hash) VALUES (?,?)",
            (username , hash_password(password))
        )
        db.commit()
        print(f"✅ User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print(f"❌ Error: Username '{username}' already exists.")
    finally:
        db.close()


"""Add the Login Function to auth.py
This will allow registered users to sign in to their accounts.
"""

def login_user(username , password):
    """
    Authenticates a user by checking their username and password.

    Args:
        username (str): The username entered by the user.
        password (str): The password entered by the user.

    Returns:
        int: The user's ID from the database if login is successful.
        None: If the username does not exist or the password is incorrect.
    """
       
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()

    # Find the user by username
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user_record = cursor.fetchone() # Fetch one matching record
    db.close()

    if user_record:
        user_id, stored_hash = user_record
        # Hash the provided password and compare it to the stored hash
        if hash_password(password) == stored_hash:
            print(f"✅ Login successful! Welcome, {username}.")
            return user_id # Return the user's ID for future use
    
    print("❌ Error: Invalid username or password.")
    return None # Return None if login fails
