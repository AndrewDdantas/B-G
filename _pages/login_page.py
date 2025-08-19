import streamlit as st
from services.connect import Service


class LoginPage:
    def __init__(self):
        self.connect = Service()
        st.title("Login")
        st.header("Please enter your credentials")
        with st.form("login_form"):
            self.username = st.text_input("Username")
            self.password = st.text_input("Password", type="password")
            self.login_button = st.form_submit_button("Login")
        if self.login_button:
            self.login()

    def login(self):
        user = self.connect.login(self.username, self.password)
        if user:
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = self.username
            st.session_state["gp_user"] = user[3]
            st.rerun()
        else:
            st.error("Invalid credentials")
