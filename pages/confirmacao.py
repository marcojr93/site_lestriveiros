import streamlit as st

st.set_page_config(page_title="Confirmação", layout="centered", initial_sidebar_state="collapsed")

st.title("✅ Inscrição Enviada!")

if "inscricao_confirmada" not in st.session_state:
    st.error("Você ainda não enviou a inscrição.")
    st.stop()

dados = st.session_state["inscricao_confirmada"]

st.success("Sua incrição será confirmada em breve")

st.markdown(f"""
- **Nome da Equipe:** {dados['equipe']}
- **Data Escolhida:** {dados['data']}
- **E-mail do Capitão:** {dados['email']}
- **Quantidade de Membros:** {dados['membros']}
""")


st.info("📬 Após confirmação, você receberá o request de pagamento através do e-mail cadastrado.")

# Botão para voltar ao menu inicial com refresh
if st.button("Voltar ao início"):
    # Limpa a sessão e faz refresh ao voltar para o início
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("homepage.py")
