import sys
import os
import streamlit as st

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui_utils import setup_page_config

setup_page_config("Confirmação Lista de Espera")

# Verifica se há dados da lista de espera confirmada
if "lista_espera_confirmada" not in st.session_state:
    st.error("Acesso inválido a esta página.")
    st.stop()

dados = st.session_state["lista_espera_confirmada"]

# Cabeçalho de sucesso
st.success("✅ **Solicitação de Lista de Espera Enviada!**")

st.title("⏰ Lista de Espera Confirmada")

# Card com informações da solicitação
st.markdown("---")
st.subheader("📋 Resumo da Solicitação")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **👥 Equipe:** {dados['equipe']}  
    **📅 Data de Preferência:** {dados['data_preferencia']}  
    **👤 Quantidade de Membros:** {dados['membros']}
    """)

with col2:
    st.markdown(f"""
    **📧 E-mail de Contato:** {dados['email']}  
    {f"**💬 Comentários:** {dados['comentarios']}" if dados['comentarios'] else "**💬 Comentários:** Nenhum"}
    """)

# Próximos passos
st.markdown("---")
st.subheader("📬 Próximos Passos")

st.info("""
**🔔 Aguarde nosso contato!**

Você foi adicionado à nossa lista de espera e receberá um e-mail caso surjam vagas disponíveis.

**⏰ Importante:**
- Mantenha seu e-mail sempre acessível
- Responda em até **24 horas** quando contactado
- O pagamento deve ser feito em até **48 horas** após confirmação
""")

# Dicas importantes
st.markdown("### 💡 Dicas Importantes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📧 Verifique seu E-mail**
    - Confira também a caixa de spam
    - Adicione nosso e-mail aos contatos
    - Mantenha notificações ativadas
    """)

with col2:
    st.markdown("""
    **⚡ Seja Rápido na Resposta**
    - Primeira resposta tem prioridade
    - Tenha os dados da equipe em mãos
    - PDetalhes de pagamento serão enviados após a confirmação
    """)

# Informações de contato
st.markdown("---")
st.subheader("📞 Contato Direto")

st.markdown("""
**Dúvidas sobre a lista de espera?**  
📧 E-mail: lestriveiros@gmail.com  
📱 Instagram: lestriveiros
""")

# Botões de navegação
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Página Inicial", use_container_width=True, type="primary"):
        # Limpa os dados da sessão
        if "lista_espera_confirmada" in st.session_state:
            del st.session_state["lista_espera_confirmada"]
        st.switch_page("main.py")

with col2:
    if st.button("🏆 Ver Ranking", use_container_width=True):
        st.switch_page("pages/ranking_anual.py")

with col3:
    if st.button("📝 Nova Solicitação", use_container_width=True):
        # Volta para homepage para escolher nova equipe
        if "equipe_nome" in st.session_state:
            del st.session_state["equipe_nome"]
        if "lista_espera_confirmada" in st.session_state:
            del st.session_state["lista_espera_confirmada"]
        st.switch_page("pages/homepage.py")
