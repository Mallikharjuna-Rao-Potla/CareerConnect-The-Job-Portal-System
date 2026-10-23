# ui/login_page.py
from pathlib import Path
from textwrap import dedent

import streamlit as st

from user_management import register_user, authenticate_user

def show():
    registration_succeeded = st.session_state.pop(
        "registration_succeeded", False
    )
    if registration_succeeded:
        st.session_state["auth_tab"] = "Sign In"
        for key in (
            "register_name",
            "register_email",
            "register_password",
            "confirm_password",
        ):
            st.session_state[key] = ""
        st.session_state["register_role"] = "candidate"

    current_dir = Path(__file__).resolve().parent
    logo_path = current_dir / "logo.png"

    st.markdown(
        dedent(
            """
            <style>
            .stApp,
            [data-testid="stAppViewContainer"] {
                background: #f5f7fb;
                color: #172033;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            #MainMenu, footer {
                visibility: hidden;
            }

            .block-container {
                max-width: 1450px;
                padding: 1.5rem 3rem 2rem;
            }

            .brand-title {
                color: #14213d;
                font-size: 2.45rem;
                font-weight: 800;
                line-height: 1.15;
                margin: 0;
                letter-spacing: -1px;
            }

            .brand-tagline {
                color: #14213d;
                font-size: 0.91rem;
                font-weight: 800;
                letter-spacing: 3px;
                margin-top: 0.45rem;
            }

            .brand-description {
                color: #727b8b;
                font-size: 1.05rem;
                text-align: right;
                padding-top: 0.3rem;
            }

            .hero-panel {
                box-sizing: border-box;
                background: linear-gradient(145deg, #142b49 0%, #193b61 100%);
                border-radius: 28px;
                padding: 3rem 2.8rem;
                min-height: 570px;
                color: #ffffff;
                box-shadow: 0 18px 45px rgba(20, 43, 73, 0.12);
            }

            .hero-eyebrow {
                color: #b8d9ff;
                font-size: 0.82rem;
                font-weight: 800;
                letter-spacing: 2.5px;
                text-transform: uppercase;
                margin-bottom: 1.8rem;
            }

            .hero-panel h1 {
                color: #ffffff !important;
                font-size: clamp(2.5rem, 4vw, 3.8rem);
                line-height: 1.12;
                font-weight: 800;
                letter-spacing: -1.5px;
                margin: 0 0 1.5rem;
            }

            .hero-panel h1 span {
                color: #68e0d3;
            }

            .hero-description {
                color: #dce7f5;
                font-size: 1.08rem;
                line-height: 1.85;
                margin-bottom: 2rem;
            }

            .hero-divider {
                border: 0;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                margin: 2rem 0;
            }

            .hero-bottom-title {
                color: #ffffff;
                font-size: 1.15rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }

            .hero-bottom-description {
                color: #c4d4e8;
                font-size: 0.98rem;
                line-height: 1.7;
            }

            .login-heading {
                color: #141d31;
                font-size: 2.5rem;
                font-weight: 800;
                letter-spacing: -1px;
                line-height: 1.2;
                margin: 0;
            }

            .login-description {
                color: #5e687a;
                font-size: 1.08rem;
                line-height: 1.7;
                margin-top: 0.9rem;
                margin-bottom: 1.2rem;
            }

            [data-testid="stWidgetLabel"] p {
                color: #202a3d !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"] {
                background-color: #ffffff !important;
                border: 1px solid #64748b !important;
                border-radius: 10px !important;
                min-height: 48px !important;
                box-shadow: none !important;
                outline: none !important;
                overflow: hidden !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"] > div {
                background-color: #ffffff !important;
                border: 0 !important;
                box-shadow: none !important;
                outline: none !important;
            }

            div[data-testid="stTextInput"] input {
                box-sizing: border-box !important;
                flex: 1 1 auto !important;
                min-width: 0 !important;
                height: 46px !important;
                line-height: 46px !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                background-color: #ffffff !important;
                color: #172033 !important;
                -webkit-text-fill-color: #172033 !important;
                caret-color: #000000 !important;
                border: 0 !important;
                box-shadow: none !important;
                font-size: 1rem !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"] button {
                align-items: center !important;
                justify-content: center !important;
                flex: 0 0 46px !important;
                width: 46px !important;
                min-width: 46px !important;
                height: 46px !important;
                margin: 0 !important;
                padding: 0 !important;
                background-color: #ffffff !important;
                color: #111827 !important;
                border: 0 !important;
                box-shadow: none !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"] button svg {
                color: #111827 !important;
                fill: #111827 !important;
                stroke: #111827 !important;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: #8793a7 !important;
                -webkit-text-fill-color: #8793a7 !important;
                opacity: 1 !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
                border: 1px solid #2563eb !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.16) !important;
                outline: none !important;
            }

            div[data-testid="stTextInput"] div[data-baseweb="input"] > div:focus-within {
                border: 0 !important;
                box-shadow: none !important;
                outline: none !important;
            }

            div[data-testid="stTextInput"] input:-webkit-autofill,
            div[data-testid="stTextInput"] input:-webkit-autofill:hover,
            div[data-testid="stTextInput"] input:-webkit-autofill:focus {
                -webkit-text-fill-color: #172033 !important;
                -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
                caret-color: #000000 !important;
            }

            div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
                display: none !important;
            }

            div[data-baseweb="popover"] li:hover {
                background-color: #dbeafe !important;
                color: #1e3a8a !important;
            }

            div[data-baseweb="popover"] li[aria-selected="true"] {
                background-color: #2563eb !important;
                color: #ffffff !important;
            }

            div.stButton > button,
            div.stFormSubmitButton > button {
                width: 100%;
                min-height: 48px;
                border: none;
                border-radius: 11px;
                background: #14847e;
                color: #ffffff;
                font-size: 1rem;
                font-weight: 700;
                transition: all 0.2s ease;
            }

            div.stButton > button:hover,
            div.stFormSubmitButton > button:hover {
                background: #106e69;
                color: #ffffff;
                border: none;
                box-shadow: 0 6px 16px rgba(20, 132, 126, 0.2);
            }

            button[data-baseweb="tab"] {
                color: #344056 !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #14847e !important;
            }

            div[data-baseweb="tab-highlight"] {
                background-color: #14847e !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 10px;
            }

            .login-footer {
                color: #7a8495;
                font-size: 0.95rem;
                line-height: 1.7;
                margin-top: 1.7rem;
                text-align: center;
            }

            @media (max-width: 900px) {
                .block-container {
                    padding-left: 1.2rem;
                    padding-right: 1.2rem;
                }

                .brand-title {
                    font-size: 1.8rem;
                }

                .brand-tagline {
                    font-size: 0.72rem;
                    letter-spacing: 2px;
                }

                .brand-description {
                    text-align: left;
                    font-size: 0.9rem;
                }

                .hero-panel {
                    min-height: auto;
                    padding: 2rem;
                }

                .hero-panel h1 {
                    font-size: 2.6rem;
                }

                .login-heading {
                    font-size: 2rem;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )

    # Header
    logo_col, brand_col = st.columns([1, 10])

    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=85)
        else:
            st.markdown("## 💼")

    with brand_col:
        st.markdown(
            dedent(
                """
                <div class="brand-title">CareerConnect</div>
                <div class="brand-tagline">YOUR CAREER. YOUR FUTURE.</div>
                """
            ),
            unsafe_allow_html=True,
        )

    st.write("")

    # Main two-column layout
    hero_col, form_col = st.columns([1.05, 1], gap="large")

    with hero_col:
        st.markdown(
            dedent(
                """
                <div class="hero-panel">
                    <div class="hero-eyebrow">Find your next opportunity</div>
                    <h1>
                        Your next<br>
                        opportunity<br>
                        starts <span>here.</span>
                    </h1>
                    <div class="hero-description">
                        Discover opportunities that match your ambitions.
                        Build meaningful connections and take the next step
                        toward a career you'll love.
                    </div>
                    <hr class="hero-divider">
                    <div class="hero-bottom-title">
                        A better way to find your future.
                    </div>
                    <div class="hero-bottom-description">
                        Explore career opportunities, connect with employers,
                        and turn your professional goals into reality.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with form_col:
        st.markdown(
            '<div class="login-heading">Welcome back</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            dedent(
                """
                <div class="login-description">
                    Sign in to your account or create one to get started.
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        sign_in_tab, create_account_tab = st.tabs(
            ["Sign In", "Create Account"],
            key="auth_tab",
            on_change="rerun",
        )

        with sign_in_tab:
            if registration_succeeded:
                st.success("Account created successfully! You can now sign in.")

            with st.form("login_form"):
                email = st.text_input(
                    "Email address",
                    placeholder="you@example.com",
                    key="login_email",
                )
                password = st.text_input(
                    "Password",
                    placeholder="Enter your password",
                    type="password",
                    key="login_password",
                )
                login_submitted = st.form_submit_button(
                    "Sign In →",
                    use_container_width=True,
                )

            if login_submitted:
                email_value = email.strip()

                if not email_value or not password:
                    st.warning("Please enter both your email address and password.")
                else:
                    try:
                        # FIXED: Unpack the return values correctly and use "user_data"
                        success, msg, user_data = authenticate_user(email_value, password)
                        if success:
                            st.session_state["logged_in"] = True
                            st.session_state["user_data"] = user_data
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(msg)
                    except Exception as exc:
                        st.error(f"Unable to sign in: {exc}")

        with create_account_tab:
            with st.form("register_form"):
                full_name = st.text_input(
                    "Full name",
                    placeholder="Enter your full name",
                    key="register_name",
                )
                register_email = st.text_input(
                    "Email address",
                    placeholder="you@example.com",
                    key="register_email",
                )
                register_password = st.text_input(
                    "Password",
                    placeholder="Create a password",
                    type="password",
                    key="register_password",
                )
                confirm_password = st.text_input(
                    "Confirm password",
                    placeholder="Re-enter your password",
                    type="password",
                    key="confirm_password",
                )
                
                # FIXED: Added the required role selector for the database
                role = st.selectbox(
                    "I am a:", 
                    ["candidate", "recruiter"], 
                    key="register_role"
                )
                
                register_submitted = st.form_submit_button(
                    "Create Account →",
                    use_container_width=True,
                )

            if register_submitted:
                name_value = full_name.strip()
                email_value = register_email.strip()

                if not name_value or not email_value:
                    st.warning("Please enter your name and email address.")
                elif not register_password:
                    st.warning("Please create a password.")
                elif register_password != confirm_password:
                    st.error("The passwords do not match.")
                else:
                    try:
                        # FIXED: Pass the role and unpack return values correctly
                        success, msg, user_id = register_user(
                            name_value,
                            email_value,
                            register_password,
                            role
                        )
                        if success:
                            st.session_state["registration_succeeded"] = True
                            st.rerun()
                        else:
                            st.error(msg)
                    except Exception as exc:
                        st.error(f"Unable to create account: {exc}")

    st.markdown(
        '<div class="login-footer">Your next career move could start right here.</div>',
        unsafe_allow_html=True,
    )