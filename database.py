# database.py
import sqlite3
import os

DB_NAME = "careerconnect.db"

def get_connection():
    """Establishes a connection to the SQLite database and enables foreign keys."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries instead of tuples
    return conn

def initialize_database():
    """Creates the necessary tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('candidate', 'recruiter')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Jobs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recruiter_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            company_name TEXT NOT NULL,
            description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            experience_required TEXT NOT NULL,
            location TEXT NOT NULL,
            employment_type TEXT NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'Closed')),
            FOREIGN KEY (recruiter_id) REFERENCES Users (user_id)
        )
    """)

    # Create Applications Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Applied' CHECK(status IN ('Applied', 'Under Review', 'Shortlisted', 'Rejected', 'Selected')),
            resume_filename TEXT,
            UNIQUE(candidate_id, job_id),
            FOREIGN KEY (candidate_id) REFERENCES Users (user_id),
            FOREIGN KEY (job_id) REFERENCES Jobs (job_id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database and tables initialized successfully.")