import streamlit as st
import smtplib
import dns.resolver

# Set default states
if "verified" not in st.session_state:
    st.session_state.verified = False

if "email_checked" not in st.session_state:
    st.session_state.email_checked = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "mobile" not in st.session_state:
    st.session_state.mobile = ""

if "email" not in st.session_state:
    st.session_state.email = ""

# SMTP validation
def check_email(email, from_email="check@yourdomain.com"):
    try:
        domain = email.split('@')[-1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(sorted(records, key=lambda r: r.preference)[0].exchange)

        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail(from_email)
        code, _ = server.rcpt(email)
        server.quit()

        return "valid" if code == 250 else "invalid"
    except Exception:
        return "error"

# --- PAGE SETTINGS ---
st.set_page_config("Viswam.ai")
st.markdown("""
<style>
/* Layout Centering */
section.main > div {
    padding-top: 2rem;
    max-width: 700px;
    margin: auto;
}

/* Enlarge input labels */
label {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: var(--text-color);
}

/* Style input fields */
.stTextInput > div > div > input {
    padding: 12px;
    font-size: 16px;
    border: 1px solid var(--secondary-background-color);
    border-radius: 0.6rem;
    background-color: var(--background-color);
    color: var(--text-color);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
    outline: none;
}

/* Placeholder text visibility in dark mode */
::placeholder {
    color: var(--text-color);
    opacity: 0.6;
}

/* Styled buttons */
.stButton > button {
    width: 100%;
    padding: 14px 24px;
    background: linear-gradient(to right, #6366f1, #4f46e5);
    color: white;
    border: none;
    border-radius: 0.6rem;
    font-weight: 700;
    font-size: 18px;
    transition: background 0.3s ease, transform 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stButton > button:hover {
    background: linear-gradient(to right, #4f46e5, #4338ca);
    transform: scale(1.01);
    cursor: pointer;
}

/* Disabled state */
.stButton > button:disabled {
    background-color: #9ca3af !important;
    color: #e5e7eb !important;
    cursor: not-allowed;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# --- HEADER ---
st.title("Email correction form - Summer Internship (Viswam.ai)")
st.markdown("we noticed that the mail has been bounced for you due to invalid email .Please enter your correct email or alternative email to get offer letter or any updates through mail.")

st.divider()

# --- FORM SECTION ---
st.subheader("User Info Form")

with st.form("email_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="enter name")
    with col2:
        mobile = st.text_input("Mobile Number", placeholder="e.g. 9876543210")

    email = st.text_input("Email Address", placeholder="e.g. user@example.com")

    verify_btn = st.form_submit_button("Verify Email")

    if verify_btn:
        if name and mobile and email:
            with st.spinner("🔎 Verifying email..."):
                result = check_email(email)
            st.session_state.email_checked = True

            if result == "valid":
                st.success("✅ Email is valid and active.")
                st.session_state.verified = True
                st.session_state.name = name
                st.session_state.mobile = mobile
                st.session_state.email = email
            elif result == "invalid":
                st.error("❌ Email is invalid or rejected by server.")
                st.session_state.verified = False
            else:
                st.warning("⚠️ Couldn't verify this email. Try again later.")
                st.session_state.verified = False
        else:
            st.warning("⚠️ Please fill all fields before verifying.")

submit_disabled = not (
    st.session_state.verified and
    st.session_state.name and
    st.session_state.mobile and
    st.session_state.email
)

submitted = st.button("Submit", disabled=submit_disabled)

if submitted:
    # Here you would call store_to_sheet or insert into a DB
    # e.g. store_to_sheet(name, mobile, email)
    st.toast("Data submitted successfully!")
    st.success(f"Thanks {st.session_state.name}! Your data has been recorded.")
    # Optionally reset verified flag or inputs
    st.session_state.verified = False
