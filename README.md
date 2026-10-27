# CareerConnect 💼 

### The Job Portal System

CareerConnect is a Python-based job portal web application designed to connect candidates with recruiters. Built using Python, Streamlit, and SQLite, it provides dedicated dashboards for job discovery, recruitment management, and application tracking.

### Live Demo: [Click here to access CareerConnect](https://careerconnect-the-job-app-system-6izavwdz5mftrvbjlmhtig.streamlit.app/)

## ✨ Key Features

* **Role-Based Access:** Separate dashboards for candidates and recruiters.
* **Smart Job Discovery:** Filter and sort job listings by location and skills.
* **Eligibility Checker:** Calculates a skill-match percentage between candidate skills and job requirements.
* **Resume Upload:** Supports PDF and DOCX resumes.
* **Application Tracking:** Enables candidates to monitor application status.
* **Recruitment Management:** Allows recruiters to post jobs, review applications, and update candidate statuses.
* **Password Security:** Uses bcrypt for password hashing.
* **Modular Architecture:** Separates UI components and backend business logic.

## 🛠️ Technology Stack

| Component            | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Frontend Framework   | Streamlit               |
| UI Styling           | Custom CSS              |
| Database             | SQLite                  |
| Database Operations  | sqlite3                 |
| Authentication       | bcrypt                  |
| Session Management   | Streamlit Session State |
| File Handling        | os, pathlib             |
| Image Processing     | Pillow (PIL)            |

## 📂 Project Structure

```text
CareerConnect/
├── app.py
├── requirements.txt
├── careerconnect.db
├── ui/
│   ├── login_page.py
│   ├── candidate_dashboard.py
│   ├── recruiter_dashboard.py
│   └── logo.png
└── modules/
    ├── user_management.py
    ├── job_management.py
    ├── application_management.py
    ├── eligibility_checker.py
    └── resume_management.py
```

## 🧩 Module Description

| Module                      | Responsibility                             |
| --------------------------- | ------------------------------------------ |
| `app.py`                    | Application entry point and global styling |
| `login_page.py`             | Login and registration interface           |
| `candidate_dashboard.py`    | Job browsing and application tracking      |
| `recruiter_dashboard.py`    | Job posting and applicant management       |
| `user_management.py`        | User registration and authentication       |
| `job_management.py`         | Job posting operations                     |
| `application_management.py` | Application processing and status updates  |
| `eligibility_checker.py`    | Candidate-job skill matching               |
| `resume_management.py`      | Resume upload and file storage             |

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mallikharjuna-Rao-Potla/CareerConnect-The-Job-Portal-System.git
cd CareerConnect-The-Job-Portal-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

## 💡 How to Use

### Candidates

1. Register with the Candidate role.
2. Log in to the candidate dashboard.
3. Browse and filter available jobs.
4. Check the skill-match percentage.
5. Upload a resume and apply for suitable positions.
6. Track application progress.

### Recruiters

1. Register with the Recruiter role.
2. Log in to the recruiter dashboard.
3. Create job postings and specify required skills.
4. Review applications and candidate resumes.
5. Update application statuses, such as Under Review, Shortlisted, or Selected.

## 🧠 Python Concepts Demonstrated

* **Modular Programming:** Organizing code into reusable modules.
* **Functions and Conditional Logic:** Implementing application workflows.
* **Data Structures:** Processing user, job, and application data.
* **Database Integration:** Performing database operations using SQLite.
* **File Handling:** Managing uploaded resumes.
* **Exception Handling:** Handling errors where implemented.
* **Session Management:** Maintaining user-specific session information.
* **Third-Party Libraries:** Integrating Streamlit, bcrypt, and Pillow.

## 🔒 Security Considerations

The application should validate user permissions, uploaded file types, and file sizes. Database queries should use parameterized statements, and sensitive information should be handled securely. Actual security depends on the implementation.

## 🔮 Future Enhancements

* AI-based job recommendations.
* Automated resume parsing and skill extraction.
* Email notifications for application updates.
* Recruitment analytics and reporting.
* Cloud deployment.
* External job listing API integration.

## 🎯 Project Objective

CareerConnect demonstrates how Python can be used to develop a modular web application with database integration, authentication, file handling, and business logic while addressing practical challenges in recruitment and job discovery.

## 👨‍💻 Project Team

* **Potla Mallikharjuna Rao** — [GitHub](https://github.com/Mallikharjuna-Rao-Potla)
* **Doguparthi Gopichand** - [GitHub](https://github.com/Gopichand-Doguparthi)
* **Yalavarthi Poorneswar** — [GitHub](https://github.com/Poorneswar999)
* **Gaddhaguti Dhana Chandra Shekar**

---

*CareerConnect — Connecting Talent with Opportunity.*
