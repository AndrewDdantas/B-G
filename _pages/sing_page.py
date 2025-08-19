import streamlit as st
from services.connect import Service


class SingPage:
    def __init__(self, gp_users, user):
        st.title("SING")
        self.connect = Service()
        if gp_users != "ADMIN":
            return False
        self.user = user

    def display(self):
        data = self.connect.get_registros_pend(
            self.user)
        data["Assinar"] = False
        data_editor = st.data_editor(
            data,
            use_container_width=True,
            num_rows="fixed",
            column_config={
                "Assinar": st.column_config.CheckboxColumn("Assinar", help="Marque a linha")
            }, hide_index=True)

        def sing_document(df):
            for index, row in df.iterrows():
                if row["Assinar"]:
                    print(self.connect.sing_document(
                        self.user, row["LIN AUX"]))
            st.success("Documentos assinados com sucesso!")
            st.rerun()
        if st.button("Assinar", use_container_width=True):
            with st.spinner("Assinando..."):
                print(sing_document(data_editor))
                st.rerun()
