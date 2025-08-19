import streamlit as st
import services.connect as connect
import uuid  # Import the uuid library
from time import sleep


class InsertPage:
    def __init__(self):
        self.connect = connect.Service()

        def logout():
            st.session_state.clear()

        with st.sidebar.container(horizontal_alignment="center", vertical_alignment="bottom"):
            st.title("Menu")
            st.write(
                f"Bem vindo! {st.session_state.get('username', '')}")
            st.button("Logout", on_click=logout,
                      use_container_width=True)

        st.title("CADASTRO DE CERTIFICADOS")
        st.subheader("Lembre-se de inserir CPFs de alunos já cadastrados.")

        if 'cpf_key' not in st.session_state:
            st.session_state.cpf_key = str(uuid.uuid4())

        cpf = st.text_input(
            "CPF do Aluno",
            key=st.session_state.cpf_key
        )

        if cpf:
            aluno = self.connect.get_aluno(cpf)
            with st.container(border=True):
                if aluno is not None:
                    col1, col2 = st.columns(2)
                    col1.text(f"Nome: {aluno['ALUNO']}")
                    col2.text(f"E-mail: {aluno['EMAIL']}")
                    self.inserir_certificado(cpf)
                else:
                    st.error("Aluno não encontrado.")

    def inserir_certificado(self, cpf):
        with st.form("my_form"):
            st.subheader("Insira os dados do certificado")
            treinamento = st.selectbox(
                "Treinamento", self.connect.get_treinamentos())
            localizacao = st.text_input(
                "Localização",
                placeholder="Ex: Brejeiro localizada na rua Aleixo Rodrigues de Queiroz - Jundiaí, Anápolis -GO",
                help="Ex: Brejeiro localizada na rua Aleixo Rodrigues de Queiroz - Jundiaí, Anápolis - GO"
            )
            data_treinamento = st.date_input(
                "Data Treinamento", format="DD/MM/YYYY")
            submit_button = st.form_submit_button("Enviar")

            if submit_button:
                if not localizacao:
                    st.error("Por favor, insira a localização do treinamento.")
                    return

                # Insere no banco
                self.connect.inserir_certificado(
                    cpf, treinamento, localizacao, data_treinamento.strftime(
                        "%d/%m/%Y")
                )

                st.success("Certificado inserido com sucesso!")
                sleep(1)

                st.session_state.cpf_key = str(uuid.uuid4())
                st.rerun()
