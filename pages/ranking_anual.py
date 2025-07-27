import sys
import os
import streamlit as st

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui_utils import setup_page_config
from data_utils import load_ranking_data, create_readable_names, get_display_columns, get_team_statistics

# Configuração da página
setup_page_config("Ranking Anual - Les Triveiros", layout="wide")
st.title("🏆 Ranking Anual - Les Triveiros")

# Carrega os dados
df = load_ranking_data()
if df is None:
    st.stop()

# Mapear colunas para nomes legíveis no dropdown (excluindo Rank e Equipe)
colunas = df.columns.tolist()
colunas_dropdown = [col for col in colunas if col not in ['Equipe', 'Rank']]

# Criar nomes legíveis para o dropdown
nomes_legiveis = create_readable_names(colunas_dropdown)

# Interface do usuário
opcao = st.selectbox(
    "Selecione a Trívia para visualização:",
    list(nomes_legiveis.values()),
    index=0
)

# Obter o nome da coluna original
coluna_selecionada = [k for k, v in nomes_legiveis.items() if v == opcao][0]

# Organizar e mostrar os dados
df_ordenado = df.sort_values(by=coluna_selecionada, ascending=False)

# Obter colunas para exibição (inclui Rank se existir)
display_columns = get_display_columns(df, coluna_selecionada)

# Melhorar a apresentação dos dados
st.subheader(f"Ranking - {opcao}")
st.dataframe(
    df_ordenado[display_columns],
    use_container_width=True,
    hide_index=True
)

# Obter estatísticas
stats = get_team_statistics(df, coluna_selecionada)

# Adicionar estatísticas atualizadas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Equipes", stats['total_teams'])
with col2:
    st.metric("🏆 Equipe com mais vitórias", stats['team_with_most_wins'])
with col3:
    st.metric("👥 Média de equipes por trívia", stats['average_teams_per_trivia'])

# Botões de navegação na parte inferior
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Voltar", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("🏠 Início", use_container_width=True):
        st.switch_page("main.py")

with col3:
    if st.button("📝 Inscrições", use_container_width=True):
        st.switch_page("pages/homepage.py")