import streamlit as st


class MainPage:
    def __init__(self, gp_user, user):
        self.gp_user = gp_user
        self.user = user

    def display(self):
        st.set_page_config(page_title="Main Page",
                           page_icon=":tada:", layout="wide")
        st.title("Bem Vindo!")

        tab1, tab2 = st.tabs(["Inserir Certificado", "Assinar Certificado"])

        with tab1:
            st.header("Inserir Certificado")
            from _pages.insert_page import InsertPage
            InsertPage()

        with tab2:
            st.header("Assinar Certificado")
            if self.gp_user == "ADMIN":
                from _pages.sing_page import SingPage
                SingPage(self.gp_user, self.user).display()
            else:
                st.error("You do not have permission to sign certificates.")
