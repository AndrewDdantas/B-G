import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st
from datetime import datetime
load_dotenv()


class Service:
    def __init__(self):
        json = {
            "type": "service_account",
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
            "universe_domain": "googleapis.com"
        }

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json, scope)
        self.client = gs.authorize(credentials)
        self.spreadsheet = self.client.open_by_key(
            "155dXO4Oq85bLOcS5GAi0DYVeJVM1gWyVw6zWu5HGLvc")

    def get_treinamentos(self):
        treinamentos = self.spreadsheet.worksheet(
            "CADASTRO TREINAMENTOS").get_values("B2:B")
        lista_treinamentos = []
        for tr in treinamentos:
            lista_treinamentos.append(tr[0])
        return lista_treinamentos

    def get_aluno(self, aluno):
        alunos = self.spreadsheet.worksheet(
            "CADASTRO ALUNOS").get_values("B2:D")
        alunos = pd.DataFrame(alunos, columns=["CPF", "ALUNO", "EMAIL"])
        aluno = alunos[alunos["CPF"] == aluno]
        if not aluno.empty:
            return aluno.iloc[0]
        return None

    def inserir_certificado(self, cpf, treinamento, localizacao, data_treinamento):
        self.spreadsheet.worksheet("REGISTRO").append_row(
            [cpf, treinamento, localizacao, data_treinamento])

    def login(self, username, password):
        users = self.spreadsheet.worksheet("USERS").get_values("B2:E")
        users = pd.DataFrame(
            users, columns=["USERNAME", "PASSWORD", "ROLE", "GP_USER"])
        user = users.loc[(users["USERNAME"] == username) &
                         (users["PASSWORD"] == password)]
        if not user.empty:
            print(user.values[0].tolist())
            return user.values[0].tolist()
        return None

    def sing_document(self, user, row):
        try:
            self.spreadsheet.worksheet(
                "REGISTRO").update([["ASSINADO", datetime.now().strftime("%d/%m/%Y %H:%M:%S")]], range_name=f"F{row}:G{row}" if user == "Bruno.Nahum"
                                   else f"H{row}:I{row}", value_input_option='USER_ENTERED')
            return True
        except Exception as e:
            print(f"Error signing document: {e}")
            return False

    def get_registros_pend(self, user):
        registros = self.spreadsheet.worksheet("REGISTRO").get_values("A:O")
        registros = pd.DataFrame(registros[1:], columns=registros[0])
        print(user)
        registros = registros[registros["ASSINATURA BRUNO"] ==
                              ""] if user == "Bruno.Nahum" else registros[registros["ASSINATURA GABRIEL"] == ""]
        return registros[["CPF", "NOME", "TREINAMENTO", "LOCALIZAÇÃO", "DATA TREINAMENTO", "LIN AUX"]]
