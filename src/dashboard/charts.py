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
df.columns

df.head()
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
        labels={"valorLiquido": "Total Gasto", "espectro_politico": "Espectro Político"},
        text_auto=True
    )
    return fig


# gráfico 2 - candidatos por espectro
def grafico_2():
    
    df_graph_2 = df_unique_id['espectro_politico'].value_counts().reset_index()
    
    fig = px.bar(
        df_graph_2,
        x='espectro_politico',
        y='count',
        title="Distribuição de Políticos por Espectro",
        text_auto=True
    )
    
    return fig


# top 10 gastos por fornecedor
def grafico_3(df, espectro=None, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]
    
    if espectro:
        df = df[df['espectro_politico'] == espectro]

    if partido:
        df = df[df['siglaPartido'] == partido]

    df_graph_3 = df.groupby(['nomeFornecedor'])['valorLiquido'].sum().nlargest(10).reset_index()

    fig = px.bar(
        df_graph_3,
        x='valorLiquido',
        y='nomeFornecedor',
        title='TOP 10 - Gastos por Fornecedor',
        text_auto=True,
        orientation='h',
    )
    #invertendo para mostrar do maior para o menor
    fig = fig.update_yaxes(categoryorder='total ascending')

    return fig



# top 10 gastos por tipo de despesa
def grafico_4(df, espectro=None, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]

    if espectro:
        df = df[df['espectro_politico'] == espectro]

    if partido:
        df = df[df['siglaPartido'] == partido]

    df_graph_3 = df.groupby(['tipoDespesa'])['valorLiquido'].sum().nlargest(10).reset_index()

    fig = px.bar(
        df_graph_3,
        x='valorLiquido',
        y='tipoDespesa',
        title='TOP 10 - Gastos por Tipo de Despesa',
        text_auto=True,
        orientation='h',
    )
    #invertendo para mostrar do maior para o menor
    fig = fig.update_yaxes(categoryorder='total ascending')

    return fig


# gráfico 5 - Sazonalidadee
def grafico_5(df, espectro=None, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]
    if espectro:
        df = df[df['espectro_politico'] == espectro]
    if partido:
        df = df[df['siglaPartido'] == partido]

    df['ano'] = pd.to_datetime(df['dataDocumento']).dt.year
    df['mes'] = pd.to_datetime(df['dataDocumento']).dt.month
    df["mes"] = df["mes"].astype(str)
    df_graph_5 = df.groupby(['ano', 'mes'])['valorLiquido'].sum().reset_index()

    fig = px.line(
        df_graph_5,
        x='mes',
        y='valorLiquido',
        color='ano',
        title='Sazonalidade dos Gastos',
        labels={'valorLiquido': '', 'mes': 'Mês'},
        markers=True,
        text='valorLiquido',
        ).update_yaxes(showticklabels=False)
        
    fig.update_traces(texttemplate='%{y:.2s}', textposition='top center')
    fig.update_layout(margin=dict(t=60, b=60))
    return fig