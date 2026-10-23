# application_management.py
import sqlite3
from database import get_connection

def apply_for_job(candidate_id, job_id, resume_filename):
    """Submits a job application for a candidate."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Applications (candidate_id, job_id, resume_filename)
            VALUES (?, ?, ?)
        """, (candidate_id, job_id, resume_filename))
        conn.commit()
        return True, "Application submitted successfully."
    except sqlite3.IntegrityError:
        # The UNIQUE(candidate_id, job_id) constraint in our DB triggers this
        return False, "You have already applied for this job."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        conn.close()

def get_candidate_applications(candidate_id):
    """Retrieves all applications submitted by a specific candidate."""
    conn = get_connection()
    cursor = conn.cursor()
    # Join Applications with Jobs to get the job title and company name
    cursor.execute("""
        SELECT a.application_id, a.application_date, a.status, a.resume_filename,
               j.title, j.company_name, j.location 
        FROM Applications a
        JOIN Jobs j ON a.job_id = j.job_id
        WHERE a.candidate_id = ?
        ORDER BY a.application_date DESC
    """, (candidate_id,))
    applications = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return applications

def get_job_applications(job_id):
    """Retrieves all applications received for a specific job."""
    conn = get_connection()
    cursor = conn.cursor()
    # Join Applications with Users to get the candidate's name and email
    cursor.execute("""
        SELECT a.application_id, a.application_date, a.status, a.resume_filename,
               u.full_name, u.email
        FROM Applications a
        JOIN Users u ON a.candidate_id = u.user_id
        WHERE a.job_id = ?
        ORDER BY a.application_date DESC
    """, (job_id,))
    applications = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return applications

def update_application_status(application_id, new_status):
    """Updates the status of a specific application."""
    valid_statuses = ['Applied', 'Under Review', 'Shortlisted', 'Rejected', 'Selected']
    if new_status not in valid_statuses:
        return False, "Invalid status."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Applications SET status = ? WHERE application_id = ?", (new_status, application_id))
        conn.commit()
        return True, "Status updated successfully."
    except Exception as e:
        return False, f"Failed to update status: {str(e)}"
    finally:
        conn.close()