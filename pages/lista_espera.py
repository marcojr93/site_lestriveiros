import sys
import os
import streamlit as st

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui_utils import setup_page_config
from email_utils import enviar_email_lista_espera

setup_page_config("Lista de Espera")

# Verifica se nome da equipe foi salvo
if "equipe_nome" not in st.session_state:
    st.error("Você deve começar pela página inicial.")
    st.stop()

st.title(f"⏰ Lista de Espera: {st.session_state['equipe_nome']}")

st.info("📝 **Lista de Espera** - Você será contatado por e-mail caso surjam vagas disponíveis!")

st.markdown("---")

# Formulário da Lista de Espera
with st.form("form_lista_espera"):
    st.subheader("📋 Informações da Equipe")
    
    # Opções de data (mesmo formato da página de inscrições)
    datas_opcoes = ["23 de julho", "25 de julho"]
    data_preferencia = st.selectbox("Data de preferência *", datas_opcoes)
    
    email_capitao = st.text_input("E-mail de contato do capitão *")
    st.caption("📩 Você será contactado neste e-mail caso surjam vagas")
    
    qtd_membros = st.selectbox("Quantidade de membros da equipe *", list(range(1, 11)))
    
    comentarios = st.text_area(
        "Comentários ou observações (opcional)", 
        placeholder="Ex: Disponibilidade para outras datas, preferências especiais, etc.",
        max_chars=300
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    enviar = st.form_submit_button("📝 Entrar na Lista de Espera", type="primary", use_container_width=True)

    if enviar:
        if not email_capitao:
            st.error("Por favor, preencha o e-mail do capitão.")
        elif "@" not in email_capitao:
            st.error("Por favor, insira um e-mail válido.")
        else:
            # Dados da lista de espera
            dados_lista_espera = {
                "equipe": st.session_state["equipe_nome"],
                "data_preferencia": data_preferencia,
                "email": email_capitao.strip(),
                "membros": qtd_membros,
                "comentarios": comentarios.strip() if comentarios else ""
            }

            try:
                # Envia apenas o e-mail (não salva no banco de dados)
                success, message = enviar_email_lista_espera(dados_lista_espera)
                
                if success:
                    # Guarda localmente e redireciona
                    st.session_state["lista_espera_confirmada"] = dados_lista_espera
                    st.success("Solicitação enviada com sucesso!")
                    st.switch_page("pages/confirmacao_lista_espera.py")
                else:
                    st.error(f"Erro ao enviar solicitação: {message}")
                    st.info("Tente novamente em alguns minutos ou entre em contato diretamente.")

            except Exception as e:
                st.error("Erro inesperado ao processar solicitação.")
                st.exception(e)

# Informações adicionais
st.markdown("---")
st.markdown("### ℹ️ Como funciona a Lista de Espera?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📧 Notificação por E-mail**
    - Você receberá um e-mail caso surjam vagas
    - Resposta rápida é importante
    - Mantenha seu e-mail sempre atualizado
    """)

with col2:
    st.markdown("""
    **⏱️ Prazo de Resposta**
    - 24 horas para confirmar interesse
    - Primeira solicitação tem prioridade
    - Instruções de pagamento serão enviadas juntamente com a confirmação
    """)

# Botões de navegação
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Voltar", use_container_width=True):
        st.switch_page("pages/inscricoes.py")

with col2:
    if st.button("🏠 Início", use_container_width=True):
        st.switch_page("main.py")

with col3:
    if st.button("🏆 Ranking", use_container_width=True):
        st.switch_page("pages/ranking_anual.py")
