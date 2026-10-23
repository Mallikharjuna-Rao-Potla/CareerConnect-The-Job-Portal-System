# resume_management.py
import os
from pathlib import Path

# Define the folder where resumes will be stored
RESUME_DIR = Path("resumes")

def ensure_resume_dir():
    """Ensures the resumes directory exists."""
    RESUME_DIR.mkdir(exist_ok=True)

def save_resume(candidate_id, file_name, file_bytes):
    """
    Saves an uploaded resume safely.
    Replaces any existing resume for this candidate to save space.
    """
    ensure_resume_dir()
    
    # Extract file extension (e.g., .pdf, .docx)
    extension = Path(file_name).suffix.lower()
    
    if extension not in ['.pdf', '.docx']:
        return False, "Invalid file format. Only PDF and DOCX are allowed.", None

    # Create a safe, standardized filename: "resume_candidate_5.pdf"
    safe_filename = f"resume_candidate_{candidate_id}{extension}"
    file_path = RESUME_DIR / safe_filename

    # Write the bytes to the file
    try:
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        return True, "Resume uploaded successfully.", safe_filename
    except Exception as e:
        return False, f"Failed to save resume: {str(e)}", None