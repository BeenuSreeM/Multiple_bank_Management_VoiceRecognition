import streamlit as st

# Simulated user database
USER_CREDENTIALS = {
    "user1": "password123",
    "admin": "admin123"
}

def login():
    """Login form for user authentication."""
    st.title("🔑 Login to Your Account")
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if st.session_state["authenticated"]:
        st.success(f"✅ Already logged in as {st.session_state['username']}")
        return
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submitted = st.form_submit_button("🔑 Login")
    
        if submitted:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("✅ Login Successful! Redirecting...")
                st.rerun()  # Updated from experimental_rerun()
            else:
                st.error("❌ Invalid credentials! Please try again.")

def logout():
    """Logout function."""
    if st.button("🚪 Logout"):
        st.session_state["authenticated"] = False
        st.session_state.pop("username", None)
        st.success("✅ Logged out successfully!")
        st.rerun()  # Updated from experimental_rerun()
