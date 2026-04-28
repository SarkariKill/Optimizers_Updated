import boto3
import streamlit as st

# -------- CONFIG --------
USER_POOL_ID = "eu-central-1_RcPgw8NcZ"
CLIENT_ID = "675bfhhin1u6s033euehmf3lf"
REGION = "eu-central-1"

client = boto3.client("cognito-idp", region_name=REGION)

# -------- SIGNUP --------
def sign_up(username, password, email):
    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )
        return True
    except Exception as e:
        st.error(f"Signup error: {e}")
        return False

# -------- LOGIN --------
def login_user(username, password):
    try:
        client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
        return True
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

# -------- VERIFY USER --------
def confirm_user(username, code):
    try:
        client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=code
        )
        return True
    except Exception as e:
        st.error(f"Verification error: {e}")
        return False

# -------- UI --------
def show_auth():
    menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

    # ---- SIGN UP ----
    if menu == "Sign Up":
        st.title("📝 Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if sign_up(email, password, email):
                st.success("Account created! Check your email for OTP.")

        st.subheader("Verify Account")
        otp = st.text_input("Enter OTP")

        if st.button("Verify"):
            if confirm_user(email, otp):
                st.success("Account verified! You can now login.")

    # ---- LOGIN ----
    elif menu == "Login":
        st.title("🔐 Login")

        username = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")