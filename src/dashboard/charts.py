import pandas as pd
import plotly.express as px
from pathlib import Path

""" ----------------CONFIGURAÇÃO DE CAMINHO---------------- """
def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)

    except PermissionError as e:
        print(f'[PERMISSION ERROR] Não foi possível criar: {path}')
        raise

    except OSError as e:
        print(f'[OS ERROR] Erro geral ao criar: {path}')
        raise
    
    else:
        print(f'[OK] Diretório {path} pronto.')


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
create_directory(DATA_DIR)



""" ----------------LEITURA DF---------------- """

csv_path = DATA_DIR / 'df_deputados.csv'
df = pd.read_csv(csv_path)

espectro_politico = {
    'PL': 'Centro-direita',
    'PT': 'Esquerda',
    'UNIÃO': 'Centro-direita',
    'PP': 'Centro-direita',
    'REPUBLICANOS': 'Direita',
    'PSD': 'Centro',
    'MDB': 'Centro',
    'PDT': 'Centro-esquerda',
    'PODE': 'Centro-direita',
    'PSB': 'Centro-esquerda',
    'PSOL': 'Esquerda',
    'PSDB': 'Centro',
    'PCdoB': 'Esquerda',
    'AVANTE': 'Centro',
    'PV': 'Centro-esquerda',
    'NOVO': 'Direita',
    'PRD': 'Direita',
    'CIDADANIA': 'Centro-esquerda',
    'SOLIDARIEDADE': 'Centro-esquerda',
    'REDE': 'Centro-esquerda'
}

# Adicionando a nova coluna com base no espectro político
df['espectro_politico'] = df['siglaPartido'].map(espectro_politico)

# criando uma variável que comporta id's únicos
df_unique_id = df.sort_values(['id']).drop_duplicates('id', keep='first')




# gráfico 1 - gastos por espectro politico
def grafico_1():

    df_graph_1 = df.groupby(['espectro_politico'])['valorLiquido'].sum().sort_values(ascending=False)
    df_graph_1 = pd.DataFrame(df_graph_1).reset_index()
    
    fig = px.bar(
        df_graph_1,
        x="espectro_politico",
        y="valorLiquido",
        title="Gastos por Espectro Político",
        labels={"valorLiquido": "Total Gasto", "espectro_politico": "Espectro Político"}
    )
    return fig


# gráfico 2 - candidatos por espectro
def grafico_2():
    
    df_graph_2 = df_unique_id['espectro_politico'].value_counts().reset_index()
    
    fig = px.pie(
        df_graph_2,
        names='espectro_politico',
        values='count',
        title="Distribuição de Políticos por Espectro"
    )
    
    return fig

