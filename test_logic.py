# test_logic.py
from user_management import register_user, authenticate_user
from job_management import get_all_open_jobs
from application_management import apply_for_job, get_candidate_applications
from eligibility_checker import calculate_match

print("--- Testing New Logic ---")

# 1. Register a Candidate
reg_success, msg, cand_id = register_user("Bob Seeker", "bob@email.com", "pass123", "candidate")
print(f"Register Candidate: {msg}")

# Authenticate Candidate
auth_success, auth_msg, cand_data = authenticate_user("bob@email.com", "pass123")

# 2. Get the Job we created earlier
jobs = get_all_open_jobs()
job_id = jobs[0]['job_id']
job_req_skills = jobs[0]['required_skills'] # Should be "Python, SQL"

# 3. Test Eligibility Checker
bob_skills = "Python, Git, HTML"
match_result = calculate_match(bob_skills, job_req_skills)
print(f"Bob's Skill Match: {match_result['match_percentage']}%")
print(f"Missing: {match_result['missing_skills']}")

# 4. Apply for the Job
if auth_success:
    app_success, app_msg = apply_for_job(cand_data['user_id'], job_id, "resume_candidate_X.pdf")
    print(f"Job Application: {app_msg}")
    
    # Try applying again to test duplicate prevention
    app_success2, app_msg2 = apply_for_job(cand_data['user_id'], job_id, "resume_candidate_X.pdf")
    print(f"Duplicate Application Test: {app_msg2}")

# 5. View Candidate's Applications
apps = get_candidate_applications(cand_data['user_id'])
print(f"Bob's Total Applications: {len(apps)}")
if apps:
    print(f"Status for '{apps[0]['title']}': {apps[0]['status']}")






'''
# test_logic.py
from database import initialize_database
from user_management import register_user, authenticate_user
from job_management import create_job, get_all_open_jobs

# 1. Initialize the DB
initialize_database()

# 2. Register a Recruiter
success, msg, user_id = register_user("Alice Recruiter", "alice@company.com", "password123", "recruiter")
print(f"Register Recruiter: {msg}")

# 3. Authenticate the Recruiter
auth_success, auth_msg, user_data = authenticate_user("alice@company.com", "password123")
print(f"Login: {auth_msg}")

# 4. Post a Job using the authenticated user's ID
if auth_success:
    job_success, job_msg = create_job(
        recruiter_id=user_data['user_id'],
        title="Python Developer",
        company_name="Tech Corp",
        description="Looking for a Python dev.",
        required_skills="Python, SQL",
        experience_required="2 years",
        location="Remote",
        employment_type="Full-time"
    )
    print(f"Job Posting: {job_msg}")

# 5. Fetch Jobs
jobs = get_all_open_jobs()
print(f"Total Open Jobs: {len(jobs)}")
for job in jobs:
    print(f"- {job['title']} at {job['company_name']}")

'''