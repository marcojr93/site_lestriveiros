import sys
import os
import streamlit as st

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