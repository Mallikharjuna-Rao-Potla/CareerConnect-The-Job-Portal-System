# ui/candidate_dashboard.py
"""Candidate-facing CareerConnect dashboard.

Keeps the existing job/application/resume integrations while refreshing the
layout, navigation, job cards, filters, and status presentation.
"""

from html import escape
import streamlit as st

from job_management import get_all_open_jobs
from application_management import apply_for_job, get_candidate_applications
from resume_management import save_resume
from eligibility_checker import calculate_match


# -------------------------------------------------------------------
# PAGE STYLING
# -------------------------------------------------------------------

def _apply_candidate_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --cc-ink: #172033;
            --cc-muted: #64748b;
            --cc-primary: #3157d5;
            --cc-border: #e1e7f0;
            --cc-surface: #ffffff;
            --cc-canvas: #f5f7fb;
        }

        [data-testid="stMain"] {
            background: var(--cc-canvas);
        }

        section[data-testid="stSidebar"] {
            background: #1e293b;
        }

        section[data-testid="stSidebar"] .st-key-candidate_logout_container {
            position: center;
            right: 1.25rem;
            bottom: 1.5rem;
            left: 1.25rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] .stRadio label {
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] .stButton > button {
            color: #ffffff;
            background: #2563eb;
            border: 0;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.16);
        }

        .cc-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1.1rem 1.4rem;
            margin: 0 0 1.6rem 0;
            background: #ffffff;
            border: 1px solid var(--cc-border);
            border-radius: 18px;
            box-shadow: 0 5px 20px rgba(15, 23, 42, 0.035);
        }

        .cc-brand {
            color: #172033;
            font-size: 1.4rem;
            line-height: 1.2;
            font-weight: 850;
            letter-spacing: -0.045em;
        }

        .cc-brand span {
            color: #3157d5;
        }

        .cc-brand-subtitle {
            color: #64748b;
            font-size: 0.84rem;
            margin-top: 0.3rem;
        }

        .cc-eyebrow {
            color: #3157d5;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.5rem;
        }

        .cc-hero {
            position: relative;
            overflow: hidden;
            padding: clamp(1.5rem, 4vw, 2.7rem);
            margin-bottom: 1.5rem;
            background: linear-gradient(120deg, #14234b 0%, #2445a5 62%, #3766dc 100%);
            border-radius: 22px;
            box-shadow: 0 14px 34px rgba(35, 67, 155, 0.17);
        }

        .cc-hero h1 {
            color: #ffffff !important;
            font-size: clamp(2rem, 4vw, 3.1rem) !important;
            line-height: 1.1 !important;
            letter-spacing: -0.045em !important;
            margin: 0 0 0.85rem 0 !important;
            max-width: 760px;
        }

        .cc-hero p {
            color: #e5edff !important;
            font-size: 1.02rem;
            max-width: 650px;
            line-height: 1.7;
            margin-bottom: 0;
        }

        .cc-hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.75rem;
            margin-bottom: 1.1rem;
            color: #eff6ff;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.23);
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .cc-section-title {
            color: #172033;
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0 0 0.25rem 0;
        }

        .cc-section-subtitle {
            color: #64748b;
            margin: 0 0 1rem 0;
            font-size: 0.94rem;
        }

        .cc-job-card, .cc-info-card, .cc-application-card {
            background: #ffffff;
            border: 1px solid var(--cc-border);
            border-radius: 16px;
            padding: 1.35rem 1.45rem;
            margin: 0 0 0.6rem 0;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.035);
        }

        .cc-job-title {
            color: #172033;
            font-size: 1.25rem;
            font-weight: 800;
            line-height: 1.35;
            margin-bottom: 0.3rem;
            overflow-wrap: anywhere;
        }

        .cc-company {
            color: #3157d5;
            font-size: 1rem;
            font-weight: 750;
            margin-bottom: 0.9rem;
            overflow-wrap: anywhere;
        }

        .cc-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem 1.15rem;
            color: #526176;
            font-size: 0.88rem;
            margin: 0.7rem 0 1rem 0;
        }

        .cc-description {
            color: #475569;
            font-size: 0.94rem;
            line-height: 1.7;
            overflow-wrap: anywhere;
        }

        .cc-skill {
            display: inline-block;
            padding: 0.3rem 0.65rem;
            margin: 0.18rem 0.25rem 0.18rem 0;
            color: #2948a0;
            background: #eef3ff;
            border: 1px solid #d9e4ff;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .cc-count {
            display: inline-block;
            padding: 0.4rem 0.75rem;
            color: #2446a7;
            background: #edf2ff;
            border: 1px solid #dce5ff;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 750;
        }

        .cc-profile-label {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.2rem;
        }

        .cc-profile-value {
            color: #172033;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            overflow-wrap: anywhere;
        }

        /* Candidate page-specific controls */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: 10px !important;
        }

        .stButton > button,
        [data-testid="stFormSubmitButton"] > button {
            border-radius: 10px !important;
            font-weight: 700 !important;
            min-height: 42px;
        }

        @media (max-width: 700px) {
            .cc-topbar {
                align-items: flex-start;
                padding: 1rem;
            }
            .cc-brand {
                font-size: 1.2rem;
            }
            .cc-job-card, .cc-info-card, .cc-application-card {
                padding: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

def logout_candidate() -> None:
    st.session_state.clear()
    st.rerun()


def _safe(value, fallback="N/A") -> str:
    """Return escaped display text to keep dynamic database content safe in HTML."""
    if value is None or str(value).strip() == "":
        value = fallback
    return escape(str(value))


def _job_signature(job: dict) -> tuple:
    return (
        str(job.get("title", "")).strip().casefold(),
        str(job.get("company_name", "")).strip().casefold(),
        str(job.get("location", "")).strip().casefold(),
    )


def _deduplicate_jobs(raw_jobs) -> list:
    jobs = []
    seen = set()
    for job in raw_jobs or []:
        signature = _job_signature(job)
        if signature not in seen:
            seen.add(signature)
            jobs.append(job)
    return jobs


def _job_card(job: dict) -> None:
    title = _safe(job.get("title"), "Untitled role")
    company = _safe(job.get("company_name"), "Company not listed")
    location = _safe(job.get("location"))
    experience = _safe(job.get("experience_required"))
    posted = _safe(str(job.get("posted_date", "N/A"))[:10])
    description_raw = str(job.get("description") or "No description provided.")
    description = _safe(
        description_raw[:220] + ("…" if len(description_raw) > 220 else "")
    )

    skills_raw = str(job.get("required_skills") or "")
    skills = [
        _safe(skill.strip())
        for skill in skills_raw.split(",")
        if skill.strip()
    ]
    skills_html = "".join(f'<span class="cc-skill">{skill}</span>' for skill in skills)
    if not skills_html:
        skills_html = '<span class="cc-skill">Skills not specified</span>'

    st.markdown(
        f"""
        <div class="cc-job-card">
            <div class="cc-job-title">{title}</div>
            <div class="cc-company">{company}</div>
            <div class="cc-meta">
                <span>💼 {experience}</span>
                <span>📍 {location}</span>
                <span>🗓️ Posted {posted}</span>
            </div>
            <div class="cc-description">{description}</div>
            <div style="margin-top: 0.85rem;">{skills_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_profile(user: dict) -> None:
    st.markdown('<div class="cc-eyebrow">Your account</div>', unsafe_allow_html=True)
    st.markdown('<div class="cc-section-title">My Profile</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cc-section-subtitle">Review the details associated with your account.</div>',
        unsafe_allow_html=True,
    )

    member_since = str(user.get("created_at") or "N/A")[:10]
    role = str(user.get("role") or "candidate").title()

    st.markdown(
        f"""
        <div class="cc-info-card">
            <div class="cc-profile-label">Full name</div>
            <div class="cc-profile-value">{_safe(user.get("full_name"))}</div>
            <div class="cc-profile-label">Email address</div>
            <div class="cc-profile-value">{_safe(user.get("email"))}</div>
            <div class="cc-profile-label">Account type</div>
            <div class="cc-profile-value">{_safe(role)}</div>
            <div class="cc-profile-label">Member since</div>
            <div class="cc-profile-value" style="margin-bottom:0;">{_safe(member_since)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_applications(user_id) -> None:
    st.markdown('<div class="cc-eyebrow">Your progress</div>', unsafe_allow_html=True)
    st.markdown('<div class="cc-section-title">My Applications</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cc-section-subtitle">Keep track of the roles you have applied for.</div>',
        unsafe_allow_html=True,
    )

    apps = get_candidate_applications(user_id)
    if not apps:
        st.info("You haven't applied to any jobs yet. Explore open roles to get started.")
        return

    st.markdown(
        f'<span class="cc-count">{len(apps)} application{"s" if len(apps) != 1 else ""}</span>',
        unsafe_allow_html=True,
    )
    st.write("")

    for index, app in enumerate(apps):
        title = _safe(app.get("title"), "Untitled role")
        company = _safe(app.get("company_name"), "Company not listed")
        location = _safe(app.get("location"))
        applied = _safe(str(app.get("application_date", "N/A"))[:10])
        status = str(app.get("status") or "Unknown")
        status_safe = _safe(status)

        st.markdown(
            f"""
            <div class="cc-application-card">
                <div class="cc-job-title">{title}</div>
                <div class="cc-company">{company}</div>
                <div class="cc-meta">
                    <span>🗓️ Applied {applied}</span>
                    <span>📍 {location}</span>
                </div>
                <div style="color:#526176;font-size:0.9rem;">
                    Current status: <strong style="color:#172033;">{status_safe}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_job_details(job: dict, user_id) -> None:
    job_id = job.get("job_id")
    st.markdown("#### Job details")
    st.write(job.get("description") or "No description provided.")

    salary_min = job.get("salary_min", "N/A")
    salary_max = job.get("salary_max", "N/A")
    st.markdown(f"**Salary range:** {salary_min} – {salary_max}")

    st.divider()
    st.markdown("#### Check your skill match")
    my_skills = st.text_input(
        "Your skills (comma-separated)",
        placeholder="e.g. Python, SQL, communication",
        key=f"skills_{job_id}",
    )

    if st.button("Check skill match", key=f"match_{job_id}", use_container_width=False):
        if my_skills.strip():
            try:
                match_data = calculate_match(my_skills, str(job.get("required_skills") or ""))
                st.progress(
                    max(0, min(100, int(match_data.get("match_percentage", 0)))) / 100
                )
                st.info(f"**Skill match: {match_data.get('match_percentage', 0)}%**")
                matching = match_data.get("matching_skills") or []
                missing = match_data.get("missing_skills") or []
                st.write(f"**Matching skills:** {', '.join(matching) if matching else 'None identified'}")
                st.write(f"**Skills to develop:** {', '.join(missing) if missing else 'None identified'}")
            except Exception as exc:
                st.error(f"Could not calculate the skill match: {exc}")
        else:
            st.warning("Enter at least one skill to check your match.")

    st.divider()
    st.markdown("#### Submit your application")
    with st.form(f"apply_form_{job_id}"):
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            help="Accepted formats: PDF and DOCX.",
            key=f"resume_{job_id}",
        )
        submit_apply = st.form_submit_button(
            "Submit application",
            use_container_width=True,
        )

        if submit_apply:
            if uploaded_file is None:
                st.warning("Please upload a resume before submitting.")
            else:
                try:
                    file_bytes = uploaded_file.getvalue()
                    save_success, save_msg, safe_filename = save_resume(
                        user_id,
                        uploaded_file.name,
                        file_bytes,
                    )
                    if not save_success:
                        st.error(save_msg)
                    else:
                        app_success, app_msg = apply_for_job(
                            user_id,
                            job_id,
                            safe_filename,
                        )
                        if app_success:
                            st.success(app_msg)
                        else:
                            st.error(app_msg)
                except Exception as exc:
                    st.error(f"Something went wrong while submitting your application: {exc}")


# -------------------------------------------------------------------
# PAGE ENTRY POINT
# -------------------------------------------------------------------

def show() -> None:
    user = st.session_state.get("user_data") or st.session_state.get("user")
    if not isinstance(user, dict):
        st.error("Your session could not be loaded. Please sign in again.")
        if st.button("Return to login"):
            logout_candidate()
        return

    user_id = user.get("user_id")
    if user_id is None:
        st.error("Your candidate account is missing its user ID. Please sign in again.")
        if st.button("Return to login", key="missing_user_id_login"):
            logout_candidate()
        return

    _apply_candidate_styles()

    with st.sidebar:
        st.markdown(
            f"""
            <h2 style="color:#f8fafc;font-size:2.2rem;margin-bottom:1.5rem;">CareerConnect</h2>
            <p style="color:#f8fafc;font-size:1.5rem;font-weight:700;margin-bottom:0.6rem;">
                Welcome,<br/>{_safe(user.get('full_name'), 'Candidate')}
            </p>
            <p style="color:#cbd5e1;font-style:italic;margin-top:0;">
                Role: {_safe(user.get('role'), 'Candidate').title()}
            </p>
            """,
            unsafe_allow_html=True,
        )
        menu_choice = st.radio(
            "Candidate navigation",
            ["Find Jobs", "My Applications", "Profile"],
            key="candidate_sidebar_navigation",
            label_visibility="collapsed",
        )
        with st.container(key="candidate_logout_container"):
            st.markdown("---")
            if st.button(
                "Logout",
                key="candidate_sidebar_logout",
                use_container_width=True,
            ):
                logout_candidate()
                return

    st.markdown(
        """
        <div class="cc-topbar">
            <div>
                <div class="cc-brand">Career<span>Connect</span></div>
                <div class="cc-brand-subtitle">Find work that moves you forward.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if menu_choice == "Profile":
        _render_profile(user)
        return

    if menu_choice == "My Applications":
        _render_applications(user_id)
        return

    # Find Jobs page
    st.markdown(
        f"""
        <div class="cc-hero">
            <div class="cc-hero-pill">✦ YOUR NEXT CHAPTER STARTS HERE</div>
            <h1>Find work that fits your future.</h1>
            <p>Explore opportunities, discover roles that match your skills, and take the next step in your career.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    raw_jobs = get_all_open_jobs()
    jobs = _deduplicate_jobs(raw_jobs)

    if not jobs:
        st.info("There are no open roles right now. Please check back soon.")
        return

    st.markdown('<div class="cc-section-title">Available opportunities</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cc-section-subtitle">Explore open roles and find your next opportunity.</div>',
        unsafe_allow_html=True,
    )

    with st.expander(" Filter and sort opportunities", expanded=True):
        f_col1, f_col2, f_col3 = st.columns([1, 1, 1.25])
        unique_locations = ["All locations"] + sorted(
            {
                str(job.get("location") or "").strip()
                for job in jobs
                if str(job.get("location") or "").strip()
            },
            key=str.casefold,
        )

        with f_col1:
            sort_order = st.selectbox(
                "Sort by",
                ["Latest first", "Oldest first"],
                key="candidate_sort_order",
            )
        with f_col2:
            filter_location = st.selectbox(
                "Location",
                unique_locations,
                key="candidate_location_filter",
            )
        with f_col3:
            filter_skill = st.text_input(
                "Required skill",
                placeholder="Try Python, SQL, design...",
                key="candidate_skill_filter",
            )

    filtered_jobs = list(jobs)

    if filter_location != "All locations":
        filtered_jobs = [
            job for job in filtered_jobs
            if str(job.get("location") or "").casefold()
            == filter_location.casefold()
        ]

    if filter_skill.strip():
        filtered_jobs = [
            job for job in filtered_jobs
            if filter_skill.strip().casefold()
            in str(job.get("required_skills") or "").casefold()
        ]

    if sort_order == "Oldest first":
        filtered_jobs.reverse()

    count_col, hint_col = st.columns([1, 2], vertical_alignment="center")
    with count_col:
        st.markdown(
            f'<span class="cc-count">Showing {len(filtered_jobs)} of {len(jobs)} unique roles</span>',
            unsafe_allow_html=True,
        )
    with hint_col:
        st.caption("Tip: use the filters to narrow roles by location or skill.")

    st.write("")

    if not filtered_jobs:
        st.warning("No opportunities match these filters. Try another location or skill.")
        return

    for job in filtered_jobs:
        _job_card(job)

        job_id = job.get("job_id")
        details_key = f"show_details_{job_id}"
        if details_key not in st.session_state:
            st.session_state[details_key] = False

        button_col, spacer_col = st.columns([1, 5])
        with button_col:
            button_label = "Close details" if st.session_state[details_key] else "View role & apply"
            if st.button(
                button_label,
                key=f"btn_apply_{job_id}",
                use_container_width=True,
            ):
                st.session_state[details_key] = not st.session_state[details_key]
                st.rerun()

        if st.session_state[details_key]:
            with st.container(border=True):
                _render_job_details(job, user_id)

        st.write("")
