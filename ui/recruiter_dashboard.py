# ui/recruiter_dashboard.py

from html import escape

import streamlit as st
from job_management import create_job, get_jobs_by_recruiter


def _safe(value, fallback="N/A"):
    if value is None or str(value).strip() == "":
        value = fallback
    return escape(str(value))


def _logout():
    st.session_state.clear()
    st.rerun()


def _render_profile(user):
    member_since = str(user.get("created_at") or "N/A")[:10]
    role = str(user.get("role") or "recruiter").title()

    st.markdown(
        '<div class="recruiter-profile-eyebrow">Your account</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="recruiter-profile-title">My Profile</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="recruiter-profile-subtitle">Review the details associated with your account.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="recruiter-profile-card">
            <div class="recruiter-profile-label">Full name</div>
            <div class="recruiter-profile-value">{_safe(user.get('full_name'))}</div>
            <div class="recruiter-profile-label">Email address</div>
            <div class="recruiter-profile-value">{_safe(user.get('email'))}</div>
            <div class="recruiter-profile-label">Account type</div>
            <div class="recruiter-profile-value">{_safe(role)}</div>
            <div class="recruiter-profile-label">Member since</div>
            <div class="recruiter-profile-value" style="margin-bottom:0;">{_safe(member_since)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show():
    # -------------------- PROFESSIONAL DESIGN --------------------
    st.markdown("""
        <style>
        /* Main dashboard background */
        .stApp {
            background-color: #f4f7fb;
        }

        /* Main content spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* Main headings */
        h1 {
            color: #17365d !important;
            font-size: 2.2rem !important;
            font-weight: 750 !important;
            letter-spacing: -0.7px;
        }

        h2, h3 {
            color: #17365d !important;
            font-weight: 650 !important;
        }

        /* Text styling */
        p, label, .stMarkdown {
            color: #334155;
        }

        /* Form and job containers */
        [data-testid="stForm"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.25rem;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        }

        /* Input fields */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background-color: #ffffff;
            color: #1e293b;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 1px #2563eb;
        }

        /* Dropdown */
        .stSelectbox div[data-baseweb="select"] > div {
            border-radius: 8px;
            border-color: #cbd5e1;
            background-color: #ffffff;
        }

        /* Buttons */
        .stButton button,
        .stFormSubmitButton button {
            background-color: #2563eb;
            color: #ffffff !important;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.4rem;
            font-weight: 600;
            transition: background-color 0.2s ease,
                        transform 0.2s ease;
        }

        .stButton button:hover,
        .stFormSubmitButton button:hover {
            background-color: #1d4ed8;
            color: #ffffff !important;
            border: none;
            transform: translateY(-1px);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #10243e;
        }

        section[data-testid="stSidebar"] * {
            color: #f1f5f9;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.5rem;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background-color: transparent;
            border-radius: 8px;
            padding: 0.6rem;
            transition: background-color 0.2s ease;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: transparent;
        }

        section[data-testid="stSidebar"] hr {
    background-color: #10243e !important;
    border: none !important;
    height: 1px !important;
    margin: 0.5rem 0 !important;
    opacity: 0.5;
}

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            min-height: calc(100vh - 1rem);
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div[data-testid="stVerticalBlock"] {
            min-height: calc(100vh - 1rem);
        }

        section[data-testid="stSidebar"] .st-key-recruiter_logout_container {
            position: sticky;
            bottom: 0;
            z-index: 1;
            margin-top: auto;
            padding-top: 1rem;
            background-color: transparent;
        }

        .recruiter-sidebar-role {
            margin: 0 0 1.4rem;
            color: #e2e8f0;
            font-size: 1rem;
            font-style: italic;
        }

        .recruiter-profile-topbar {
            padding: 1.1rem 1.4rem;
            margin: 0 0 1.6rem;
            background: #ffffff;
            border: 1px solid #e1e7f0;
            border-radius: 18px;
            box-shadow: 0 5px 20px rgba(15, 23, 42, 0.035);
        }

        .recruiter-profile-brand {
            color: #172033;
            font-size: 1.4rem;
            line-height: 1.2;
            font-weight: 850;
            letter-spacing: -0.045em;
        }

        .recruiter-profile-brand span {
            color: #3157d5;
        }

        .recruiter-profile-brand-subtitle {
            margin-top: 0.3rem;
            color: #64748b;
            font-size: 0.84rem;
        }

        .recruiter-profile-eyebrow {
            margin-bottom: 0.5rem;
            color: #3157d5;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .recruiter-profile-title {
            margin-bottom: 0.25rem;
            color: #172033;
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .recruiter-profile-subtitle {
            margin-bottom: 1rem;
            color: #64748b;
            font-size: 0.94rem;
        }

        .recruiter-profile-card {
            padding: 1.35rem 1.45rem;
            margin-bottom: 0.6rem;
            background: #ffffff;
            border: 1px solid #e1e7f0;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.035);
        }

        .recruiter-profile-label {
            margin-bottom: 0.2rem;
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .recruiter-profile-value {
            margin-bottom: 1rem;
            color: #172033;
            font-size: 1rem;
            font-weight: 600;
            overflow-wrap: anywhere;
        }

        /* Form labels */
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label {
            color: #334155 !important;
            font-weight: 600;
        }

        /* Horizontal separators */
        hr {
            border-color: #e2e8f0;
        }

        /* Alerts */
        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Responsive spacing */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }

            h1 {
                font-size: 1.7rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user_data") or st.session_state.get("user") or {}
    user_id = user.get("user_id")

    # -------------------- SIDEBAR NAVIGATION --------------------
    with st.sidebar:
        st.markdown(
            """
            <h2 style="color:#f8fafc;font-size:2rem;margin-bottom:1.4rem;">
                CareerConnect
            </h2>
            <p style="color:#f8fafc;font-size:1.5rem;font-weight:700;margin-bottom:0.6rem;">
                Welcome,
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="color:#f8fafc;font-size:1.5rem;font-weight:700;margin-bottom:0.6rem;overflow-wrap:anywhere;">'
            f'{_safe(user.get("full_name"), "Recruiter")}</p>'
            f'<p class="recruiter-sidebar-role">Role: {_safe(user.get("role"), "Recruiter").title()}</p>',
            unsafe_allow_html=True,
        )
        choice = st.radio(
            "Recruiter navigation",
            ["Post a Job", "My Posted Jobs", "Profile"],
            key="recruiter_sidebar_navigation",
            label_visibility="collapsed",
        )
        with st.container(key="recruiter_logout_container"):
            st.markdown(
                """
                <div style="
                    height: 1px;
                    background-color: rgba(248, 250, 252, 0.2);
                    margin-bottom: 1rem;
                "></div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Logout",
                key="recruiter_sidebar_logout",
                use_container_width=True,
            ):
                _logout()
                return

    # -------------------- DASHBOARD HEADER --------------------
    if choice == "Profile":
        st.markdown(
            """
            <div class="recruiter-profile-topbar">
                <div class="recruiter-profile-brand">Career<span>Connect</span></div>
                <div class="recruiter-profile-brand-subtitle">
                    Manage job postings and connect with the right talent.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(120deg, #17365d, #2563eb);
            padding: 1.8rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.8rem;
            box-shadow: 0 8px 22px rgba(23, 54, 93, 0.15);
        ">
            <div style="
                color: #bfdbfe;
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 0.5rem;
            ">
                CAREERCONNECT · RECRUITER PORTAL
            </div>
            <div style="
                color: #ffffff;
                font-size: 2rem;
                font-weight: 750;
                margin-bottom: 0.4rem;
            ">
                Recruiter Dashboard
            </div>
            <div style="
                color: #e2e8f0;
                font-size: 1rem;
            ">
                Manage job postings and connect with the right talent.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------- POST A JOB --------------------
    if choice == "Post a Job":

        st.markdown("""
            <div style="margin-bottom: 1.2rem;">
                <div style="
                    color: #17365d;
                    font-size: 1.55rem;
                    font-weight: 700;
                ">
                    Create a Job Posting
                </div>
                <div style="
                    color: #64748b;
                    font-size: 0.95rem;
                    margin-top: 0.3rem;
                ">
                    Enter the job details below to publish an opportunity.
                    Fields marked with * are required.
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("post_job_form"):

            st.markdown("#### Job Information")
            st.caption("Provide the position and company details.")

            title = st.text_input(
                "Job Title*",
                placeholder="e.g., Python Developer"
            )

            company_name = st.text_input(
                "Company Name*",
                placeholder="e.g., ABC Technologies"
            )

            location = st.text_input(
                "Location*",
                placeholder="e.g., Hyderabad, India"
            )

            employment_type = st.selectbox(
                "Employment Type",
                [
                    "Full-time",
                    "Part-time",
                    "Contract",
                    "Internship"
                ]
            )

            st.markdown("---")
            st.markdown("#### Job Requirements")
            st.caption("Describe the responsibilities and required qualifications.")

            description = st.text_area(
                "Job Description*",
                placeholder="Describe the role, responsibilities, and expectations...",
                height=150
            )

            required_skills = st.text_input(
                "Required Skills* (comma-separated, e.g., Python, SQL)",
                placeholder="Python, SQL, Data Analysis"
            )

            experience_required = st.text_input(
                "Experience Required* (e.g., 2 years)",
                placeholder="e.g., 2 years"
            )

            st.markdown("---")
            st.markdown("#### Compensation")
            st.caption("Specify the salary range for this position.")

            # Keep the existing salary inputs side by side
            col1, col2 = st.columns(2)

            with col1:
                salary_min = st.number_input(
                    "Minimum Salary",
                    min_value=0,
                    step=1000
                )

            with col2:
                salary_max = st.number_input(
                    "Maximum Salary",
                    min_value=0,
                    step=1000
                )

            st.markdown("<br>", unsafe_allow_html=True)

            submit = st.form_submit_button(
                "Publish Job Posting",
                use_container_width=True
            )

            if submit:
                # Existing validation preserved
                if (
                    title
                    and company_name
                    and description
                    and required_skills
                    and experience_required
                    and location
                ):
                    success, msg = create_job(
                        recruiter_id=user_id,
                        title=title,
                        company_name=company_name,
                        description=description,
                        required_skills=required_skills,
                        experience_required=experience_required,
                        location=location,
                        employment_type=employment_type,
                        salary_min=salary_min,
                        salary_max=salary_max
                    )

                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

                else:
                    st.warning(
                        "Please fill in all required fields marked with *."
                    )

    # -------------------- MY POSTED JOBS --------------------
    elif choice == "My Posted Jobs":

        st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <div style="
                    color: #17365d;
                    font-size: 1.55rem;
                    font-weight: 700;
                ">
                    My Posted Jobs
                </div>
                <div style="
                    color: #64748b;
                    font-size: 0.95rem;
                    margin-top: 0.3rem;
                ">
                    Review the job opportunities you have published.
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Retrieve jobs using the existing database function
        jobs = get_jobs_by_recruiter(user_id)

        if not jobs:
            st.info("You haven't posted any jobs yet.")

        else:
            for job in jobs:
                with st.container(border=True):

                    # Job title and company
                    st.markdown(
                        f"""
                        <div style="
                            color: #17365d;
                            font-size: 1.3rem;
                            font-weight: 700;
                            margin-bottom: 0.3rem;
                        ">
                            {job['title']}
                        </div>
                        <div style="
                            color: #64748b;
                            font-size: 1rem;
                            margin-bottom: 1rem;
                        ">
                            {job['company_name']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Location and employment type
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Location**")
                        st.write(job['location'])

                    with col2:
                        st.markdown("**Employment Type**")
                        st.write(job['employment_type'])

                    st.markdown("---")

                    # Required skills
                    st.markdown("**Required Skills**")
                    st.write(job['required_skills'])

                    # Existing status and posting date
                    st.caption(
                        f"Status: {job['status']} | "
                        f"Posted on: {job['posted_date']}"
                    )

    elif choice == "Profile":
        _render_profile(user)