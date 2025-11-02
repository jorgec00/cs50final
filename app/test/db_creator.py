import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Create a function to initialize the database
def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            pwd_hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Create a function to add a user (for testing purposes)
def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    pwd_hash = generate_password_hash(password)

    c.execute('INSERT INTO users (username, pwd_hash) VALUES (?, ?)', (username, pwd_hash))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    add_user('testuser', 'testpassword')
    print("Database created successfully.")