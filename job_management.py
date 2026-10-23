# job_management.py
from database import get_connection

def create_job(recruiter_id, title, company_name, description, required_skills, experience_required, location, employment_type, salary_min=None, salary_max=None):
    """Creates a new job posting in the database."""
    if not all([title, company_name, description, required_skills, location]):
        raise ValueError("Core job details cannot be empty.")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Jobs (recruiter_id, title, company_name, description, required_skills, 
                              experience_required, location, employment_type, salary_min, salary_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (recruiter_id, title, company_name, description, required_skills, 
              experience_required, location, employment_type, salary_min, salary_max))
        conn.commit()
        return True, "Job posted successfully."
    except Exception as e:
        return False, f"Failed to post job: {str(e)}"
    finally:
        conn.close()

def get_all_open_jobs():
    """Retrieves all jobs that are currently open."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Jobs WHERE status = 'Open' ORDER BY posted_date DESC")
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jobs

def get_jobs_by_recruiter(recruiter_id):
    """Retrieves all jobs posted by a specific recruiter."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Jobs WHERE recruiter_id = ? ORDER BY posted_date DESC", (recruiter_id,))
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jobs