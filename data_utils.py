import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_ranking_data():
    """Carrega dados do ranking com cache."""
    try:
        # Tenta carregar da nova estrutura primeiro
        file_path = os.path.join("assets", "ranking_anual.xlsx")
        if not os.path.exists(file_path):
            # Fallback para o caminho atual durante a transição
            file_path = "ranking_anual.xlsx"
            if not os.path.exists(file_path):
                st.error("Arquivo ranking_anual.xlsx não encontrado!")
                return None
        
        df = pd.read_excel(file_path)
        
        # Validação básica dos dados
        if df.empty:
            st.error("Arquivo de ranking está vazio!")
            return None
            
        if 'Equipe' not in df.columns:
            st.error("Coluna 'Equipe' não encontrada no arquivo!")
            return None
            
        return df
        
    except FileNotFoundError:
        st.error("Arquivo de ranking não encontrado. Verifique se o arquivo 'ranking_anual.xlsx' existe.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados do ranking: {e}")
        return None

def create_readable_names(columns):
    """Cria nomes legíveis para as colunas do dropdown."""
    nomes_legiveis = {}
    
    for col in columns:
        if col == "TOTAL":
            nomes_legiveis[col] = "📊 Ranking Anual"
        elif "TRIVIA" in col.upper():
            # Remove "TRIVIA" e formata o nome
            nome_limpo = col.replace("TRIVIA", "").replace("trivia", "").strip()
            if nome_limpo:
                nomes_legiveis[col] = f"🎯 Trívia {nome_limpo}"
            else:
                nomes_legiveis[col] = f"🎯 {col}"
        else:
            # Para outras colunas, apenas capitaliza
            nomes_legiveis[col] = col.title()
    
    return nomes_legiveis

def get_display_columns(df, selected_column):
    """Retorna as colunas a serem exibidas no dataset incluindo Rank se existir."""
    if df is None:
        return []
    
    # Colunas básicas a serem sempre exibidas
    display_columns = []
    
    # Adiciona Rank se existir
    if 'Rank' in df.columns:
        display_columns.append('Rank')
    
    # Sempre inclui Equipe
    if 'Equipe' in df.columns:
        display_columns.append('Equipe')
    
    # Adiciona a coluna selecionada se for diferente das já incluídas
    if selected_column not in display_columns:
        display_columns.append(selected_column)
    
    return display_columns

def validate_ranking_data(df):
    """Valida se os dados do ranking estão no formato correto."""
    if df is None:
        return False, "DataFrame é None"
    
    if df.empty:
        return False, "DataFrame está vazio"
    
    required_columns = ['Equipe']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Colunas obrigatórias ausentes: {missing_columns}"
    
    # Verifica se há pelo menos uma coluna de pontuação
    score_columns = [col for col in df.columns if col not in ['Equipe', 'Rank']]
    if not score_columns:
        return False, "Nenhuma coluna de pontuação encontrada"
    
    return True, "Dados válidos"

def get_team_with_most_wins(df):
    """Retorna a equipe que ganhou mais trívias individuais."""
    if df is None:
        return "N/A"
    
    # Pega apenas colunas de trívias (exclui Equipe, Rank e TOTAL)
    trivia_columns = [col for col in df.columns if col not in ['Equipe', 'Rank', 'TOTAL']]
    
    if not trivia_columns:
        return "N/A"
    
    # Conta quantas vezes cada equipe ficou em 1º lugar
    wins_count = {}
    
    for col in trivia_columns:
        # Encontra a equipe com maior pontuação nesta trívia
        if col in df.columns and not df[col].isna().all():
            max_score = df[col].max()
            winners = df[df[col] == max_score]['Equipe'].tolist()
            
            # Se houver empate, conta para todas as equipes empatadas
            for winner in winners:
                wins_count[winner] = wins_count.get(winner, 0) + 1
    
    if not wins_count:
        return "N/A"
    
    # Encontra a equipe com mais vitórias
    max_wins = max(wins_count.values())
    champions = [team for team, wins in wins_count.items() if wins == max_wins]
    
    if len(champions) == 1:
        return f"{champions[0]} ({max_wins} vitórias)"
    else:
        # Em caso de empate, mostra todas as equipes
        return f"{', '.join(champions)} ({max_wins} vitórias cada)"

def get_average_teams_per_trivia(df):
    """Calcula a média de equipes que participaram por trívia."""
    if df is None:
        return 0
    
    # Pega apenas colunas de trívias (exclui Equipe, Rank e TOTAL)
    trivia_columns = [col for col in df.columns if col not in ['Equipe', 'Rank', 'TOTAL']]
    
    if not trivia_columns:
        return 0
    
    total_participants = 0
    valid_trivias = 0
    
    for col in trivia_columns:
        if col in df.columns:
            # Conta equipes que participaram (pontuação > 0)
            participants = len(df[df[col] > 0])
            if participants > 0:
                total_participants += participants
                valid_trivias += 1
    
    if valid_trivias == 0:
        return 0
    
    return round(total_participants / valid_trivias, 1)

def get_team_statistics(df, column):
    """Retorna estatísticas básicas para uma coluna específica."""
    if df is None or column not in df.columns:
        return None
    
    stats = {
        'total_teams': len(df),
        'team_with_most_wins': get_team_with_most_wins(df),
        'average_teams_per_trivia': get_average_teams_per_trivia(df),
        'max_score': df[column].max(),
        'min_score': df[column].min(),
        'average_score': df[column].mean(),
        'median_score': df[column].median(),
        'std_score': df[column].std()
    }
    
    return stats

def filter_top_teams(df, column, n=10):
    """Retorna as top N equipes para uma coluna específica."""
    if df is None or column not in df.columns:
        return None
    
    # Inclui Rank na exibição se existir
    columns_to_show = ['Equipe', column]
    if 'Rank' in df.columns:
        columns_to_show.insert(0, 'Rank')
    
    return df.nlargest(n, column)[columns_to_show]

def get_team_ranking(df, team_name, column):
    """Retorna a posição de uma equipe específica no ranking."""
    if df is None or column not in df.columns:
        return None
    
    df_sorted = df.sort_values(by=column, ascending=False).reset_index(drop=True)
    
    try:
        position = df_sorted[df_sorted['Equipe'] == team_name].index[0] + 1
        return position
    except IndexError:
        return None

@st.cache_data
def process_ranking_data(file_path):
    """Processa e limpa os dados do ranking."""
    try:
        df = pd.read_excel(file_path)
        
        # Remove linhas vazias
        df = df.dropna(subset=['Equipe'])
        
        # Remove espaços extras dos nomes das equipes
        df['Equipe'] = df['Equipe'].str.strip()
        
        # Converte colunas numéricas (exceto Equipe)
        numeric_columns = df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            if col not in ['Equipe']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Garante que Rank seja inteiro se existir
        if 'Rank' in df.columns:
            df['Rank'] = df['Rank'].astype(int)
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return None
