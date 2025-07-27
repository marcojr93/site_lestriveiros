import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import os

def center_image(image_path, width=300):
    """Centraliza uma imagem na página."""
    # Ajusta o caminho para a nova estrutura
    full_path = os.path.join("assets", "images", image_path)
    
    if not os.path.exists(full_path):
        st.error(f"Imagem não encontrada: {full_path}")
        return
    
    img = Image.open(full_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_b64}' width='{width}'/>
        </div>
    """, unsafe_allow_html=True)

def setup_page_config(title="Les Triveiros", layout="centered"):
    """Configuração padrão das páginas."""
    st.set_page_config(
        page_title=title, 
        layout=layout, 
        initial_sidebar_state="collapsed"  # Sidebar inicia fechado
    )
    
    # CSS para ocultar completamente o sidebar
    st.markdown("""
    <style>
    /* Oculta o sidebar completamente */
    .css-1d391kg {display: none}
    .css-1rs6os {display: none}
    .css-17eq0hr {display: none}
    section[data-testid="stSidebar"] {display: none}
    
    /* Ajusta o conteúdo principal para ocupar toda a largura */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: none;
    }
    </style>
    """, unsafe_allow_html=True)