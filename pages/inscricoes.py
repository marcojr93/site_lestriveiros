import sys
import os
import streamlit as st

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from firebase_config import get_firestore_client
from ui_utils import setup_page_config
from email_utils import enviar_email_inscricao

setup_page_config("Formulário de Inscrição")

# Verifica se nome da equipe foi salvo
if "equipe_nome" not in st.session_state:
    st.error("Você deve começar pela página inicial.")
    st.stop()

st.title(f"📋 Inscrição da Equipe: {st.session_state['equipe_nome']}")

# 🔎 Busca número de inscrições por data
try:
    db = get_firestore_client()
    datas = ["24 de Agosto"]
    contagem_datas = {}
    vagas_totais = 10

    for data in datas:
        equipes = db.collection("inscricoes_trivia").document(data).collection("equipes").stream()
        qtd = sum(1 for _ in equipes)
        contagem_datas[data] = qtd

except Exception as e:
    st.error("Erro ao conectar com o Firebase.")
    st.exception(e)
    st.stop()

# Lista com rótulo personalizado
datas_disponiveis = []
for data in datas:
    vagas_restantes = vagas_totais - contagem_datas[data]
    if vagas_restantes > 0:
        datas_disponiveis.append(f"{data} ({vagas_restantes} vaga(s) restante(s))")

# Verifica se todas as datas estão lotadas
if not datas_disponiveis:
    st.warning("⚠️ Todas as datas estão com lotação máxima.")
    st.info("🔔 As inscrições estão encerradas no momento.")
    
    # Destaque para lista de espera
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Ainda quer participar?** Entre na lista de espera e seja notificado caso surjam vagas!")
    
    # Botão principal para lista de espera
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Entrar na Lista de Espera", use_container_width=True, type="primary"):
            st.switch_page("pages/lista_espera.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Outros botões de navegação
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            st.switch_page("main.py")
    
    with col2:
        if st.button("🏆 Ver Ranking", use_container_width=True):
            st.switch_page("pages/ranking_anual.py")
    
    with col3:
        if st.button("⬅️ Voltar à página anterior", use_container_width=True):
            st.switch_page("pages/homepage.py")
    
    st.stop()

# Formulário (só executa se há vagas disponíveis)
with st.form("form_inscricao"):
    data_formatada = st.selectbox("Data da Trívia *", datas_disponiveis)
    email_capitao = st.text_input("E-mail de contato do capitão *")
    st.caption("📩 Necessário para envio do Interac para pagamento")
    qtd_membros = st.selectbox("Quantidade de membros da equipe *", list(range(1, 11)))

    enviar = st.form_submit_button("Enviar Inscrição ✅", type="primary")

    if enviar:
        if not email_capitao:
            st.error("Por favor, preencha o e-mail do capitão.")
        else:
            # Extrai apenas a data (sem o texto de vagas restantes)
            data_limpa = data_formatada.split(" (")[0]

            # Revalida a quantidade de inscritos
            equipes = db.collection("inscricoes_trivia").document(data_limpa).collection("equipes").stream()
            count = sum(1 for _ in equipes)
            if count >= vagas_totais:
                st.error(f"A data {data_limpa} atingiu o limite de {vagas_totais} equipes. Escolha outra data.")
                st.stop()

            # Dados da inscrição
            dados_inscricao = {
                "equipe": st.session_state["equipe_nome"],
                "data": data_limpa,
                "email": email_capitao.strip(),
                "membros": qtd_membros
            }

            try:
                # Salva em subcoleção por data
                db.collection("inscricoes_trivia").document(data_limpa).collection("equipes").add(dados_inscricao)

                # Envia e-mail para o organizador
                success, message = enviar_email_inscricao(dados_inscricao)
                if not success:
                    st.warning(f"Inscrição salva, mas erro no e-mail: {message}")

                # Guarda localmente e redireciona
                st.session_state["inscricao_confirmada"] = dados_inscricao
                st.success("Inscrição enviada com sucesso!")
                st.switch_page("pages/confirmacao.py")

            except Exception as e:
                st.error("Erro ao salvar no Firebase.")
                st.exception(e)

# Botões de navegação na parte inferior (só mostra se formulário está disponível)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Voltar", use_container_width=True):
        st.switch_page("pages/homepage.py")

with col2:
    if st.button("🏠 Início", use_container_width=True):
        st.switch_page("main.py")

with col3:
    if st.button("🏆 Ranking", use_container_width=True):
        st.switch_page("pages/ranking_anual.py")


