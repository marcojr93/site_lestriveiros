import streamlit as st
from firebase_config import get_firestore_client

st.set_page_config(page_title="Formulário de Inscrição", layout="centered", initial_sidebar_state="collapsed")

# Verifica se nome da equipe foi salvo
if "equipe_nome" not in st.session_state:
    st.error("Você deve começar pela página inicial.")
    st.stop()

st.title(f"📋 Inscrição da Equipe: {st.session_state['equipe_nome']}")

# 🔎 Busca número de inscrições por data
try:
    db = get_firestore_client()
    datas = ["23 de julho", "25 de julho"]
    contagem_datas = {}
    vagas_totais = 6

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

if not datas_disponiveis:
    st.warning("⚠️ Todas as datas estão com lotação máxima (6 equipes). Inscrições encerradas.")
    st.stop()

# Formulário
with st.form("form_inscricao"):
    data_formatada = st.selectbox("Data da Trívia *", datas_disponiveis)
    email_capitao = st.text_input("E-mail de contato do capitão *")
    st.caption("📩 Necessário para envio do Interac para pagamento")
    qtd_membros = st.selectbox("Quantidade de membros da equipe *", list(range(1, 11)))

    enviar = st.form_submit_button("Enviar Inscrição ✅")

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

                # Guarda localmente e redireciona
                st.session_state["inscricao_confirmada"] = dados_inscricao
                st.success("Inscrição enviada com sucesso!")
                st.switch_page("pages/confirmacao.py")

            except Exception as e:
                st.error("Erro ao salvar no Firebase.")
                st.exception(e)
