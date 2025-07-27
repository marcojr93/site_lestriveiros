import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def enviar_email_inscricao(dados_inscricao):
    """Envia email de notificação de nova inscrição."""
    try:
        remetente = os.getenv('EMAIL_SENDER', 'lestriveiros@gmail.com')
        senha = os.getenv('EMAIL_PASSWORD')
        destinatario = os.getenv('EMAIL_DESTINATARIO', 'bianca.s.cordeiro@gmail.com')
        
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