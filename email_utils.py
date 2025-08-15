import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def enviar_email_inscricao(dados_inscricao):
    """Envia email de notificação de nova inscrição."""
    try:
        remetente = st.secrets["email"]["EMAIL_SENDER"]
        senha = st.secrets["email"]["EMAIL_PASSWORD"]
        destinatario = st.secrets["email"]["EMAIL_DESTINATARIO"]

        if not senha:
            raise ValueError("Senha do email não configurada")

        assunto = f"Nova inscrição: {dados_inscricao['equipe']} ({dados_inscricao['data']})"
        corpo = f"""
Nova inscrição recebida:

Equipe: {dados_inscricao['equipe']}
Data: {dados_inscricao['data']}
E-mail do capitão: {dados_inscricao['email']}
Quantidade de membros: {dados_inscricao['membros']}
"""

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())

        return True, "Email enviado com sucesso"
    except Exception as e:
        return False, str(e)

def enviar_email_lista_espera(dados_lista_espera):
    """Envia email de notificação de nova solicitação de lista de espera."""
    try:
        remetente = st.secrets["email"]["EMAIL_SENDER"]
        senha = st.secrets["email"]["EMAIL_PASSWORD"]
        destinatario = st.secrets["email"]["EMAIL_DESTINATARIO"]

        if not senha:
            raise ValueError("Senha do email não configurada")

        assunto = f"🔔 LISTA DE ESPERA: {dados_lista_espera['equipe']} ({dados_lista_espera['data_preferencia']})"
        corpo = f"""
⏰ NOVA SOLICITAÇÃO DE LISTA DE ESPERA

Equipe: {dados_lista_espera['equipe']}
Data de preferência: {dados_lista_espera['data_preferencia']}
E-mail do capitão: {dados_lista_espera['email']}
Quantidade de membros: {dados_lista_espera['membros']}

{f"Comentários: {dados_lista_espera['comentarios']}" if dados_lista_espera.get('comentarios') else "Sem comentários adicionais"}

---
Esta é uma solicitação de LISTA DE ESPERA. Entre em contato caso surjam vagas disponíveis.
"""

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())

        return True, "Email da lista de espera enviado com sucesso"
    except Exception as e:
        return False, str(e)