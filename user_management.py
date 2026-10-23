# user_management.py
import sqlite3
import bcrypt
from database import get_connection

def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against the stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(full_name, email, password, role):
    """Registers a new user in the database."""
    if not all([full_name, email, password, role]):
        raise ValueError("All fields are required.")
    
    if role not in ['candidate', 'recruiter']:
        raise ValueError("Invalid role specified.")

    hashed_pw = hash_password(password)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (full_name.strip(), email.strip().lower(), hashed_pw, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return True, "Registration successful.", user_id
    except sqlite3.IntegrityError:
        return False, "Email already exists.", None
    finally:
        conn.close()

def authenticate_user(email, password):
    """Authenticates a user and returns their user record if successful."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()

    if user and check_password(password, user['password_hash']):
        # Convert sqlite3.Row to a standard dictionary to safely pass around
        return True, "Login successful.", dict(user)
    
    return False, "Invalid email or password.", None