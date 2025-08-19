import streamlit as st
from _pages.login_page import LoginPage
from _pages.main_page import MainPage

if st.session_state.get("logged_in"):
    MainPage(st.session_state.get("gp_user"),
             st.session_state.get("username")).display()
else:
    LoginPage()
