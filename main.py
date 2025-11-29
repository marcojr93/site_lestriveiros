import sys
import os
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui_utils import center_image, setup_page_config

setup_page_config("Les Triveiros")

# CSS para ocultar sidebar globalmente
st.markdown("""
<style>
/* Oculta sidebar e botão de expansão */
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}

/* Otimiza layout sem sidebar */
.main .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: none;
}
</style>
""", unsafe_allow_html=True)

# Exibe a logo centralizada
center_image("logo.png", width=300)

st.title("Navegue pelo menu para ver ranking atualizado e inscrições para as próximas Trívias!")

# Botões de navegação
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    if st.button("📝 Inscrições para próxima Trívia", use_container_width=True):
        st.switch_page("pages/homepage.py")  

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏆 Ranking Anual", use_container_width=True):
        st.switch_page("pages/ranking_anual.py")  

    st.markdown("</div>", unsafe_allow_html=True)

# Rodapé com ícones de contato
st.markdown("<br><br>", unsafe_allow_html=True)

# Carrega e converte ícones para base64
zaplogo_path = os.path.join("assets", "images", "zaplogo.png")
logomail_path = os.path.join("assets", "images", "logomail.png")

zaplogo_img = Image.open(zaplogo_path)
logomail_img = Image.open(logomail_path)

buffered_zap = BytesIO()
zaplogo_img.save(buffered_zap, format="PNG")
zaplogo_b64 = base64.b64encode(buffered_zap.getvalue()).decode()

buffered_mail = BytesIO()
logomail_img.save(buffered_mail, format="PNG")
logomail_b64 = base64.b64encode(buffered_mail.getvalue()).decode()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='display: flex; justify-content: center; align-items: center; gap: 30px;'>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <img src='data:image/png;base64,{zaplogo_b64}' width='30' style='vertical-align: middle;'/>
                <a href='https://chat.whatsapp.com/FihA4w8STxsDRxreHDSzad' target='_blank' style='text-decoration: none; color: #ffffff; font-size: 12px;'>Entre na comunidade</a>
            </div>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <img src='data:image/png;base64,{logomail_b64}' width='30' style='vertical-align: middle;'/>
                <a href='mailto:lestriveiros@gmail.com' style='text-decoration: none; color: #ffffff; font-size: 12px;'>Contato via e-mail</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)