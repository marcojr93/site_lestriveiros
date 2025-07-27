import streamlit as st

st.set_page_config(page_title="Inscrição | Les Triveiros", layout="centered", initial_sidebar_state="collapsed")

# Exibe a logo centralizada no topo da página usando st.image e alinhamento
import base64
from io import BytesIO
from PIL import Image

def center_image(image_path, width=300):
    # Tenta primeiro o caminho da nova estrutura
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        # Fallback para o caminho antigo
        img = Image.open("logo.png")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_b64}' width='{width}'/>
        </div>
    """, unsafe_allow_html=True)

center_image("assets/images/logo.png", width=300)

st.title("Garanta sua equipe em nossa próxima Trívia!")

st.markdown("Para começar, informe o **nome da equipe**:")

nome_equipe = st.text_input("Nome da Equipe *")

if "equipe_nome" not in st.session_state:
    if nome_equipe:
        if st.button("Avançar ➡️", type="primary"):
            st.session_state["equipe_nome"] = nome_equipe.strip()
            st.switch_page("pages/inscricoes.py")
    else:
        st.warning("⚠️ Por favor, informe o nome da equipe para continuar.")

# Botões de navegação na parte inferior
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Voltar ao Início", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("🏆 Ver Ranking", use_container_width=True):
        st.switch_page("pages/ranking_anual.py")


