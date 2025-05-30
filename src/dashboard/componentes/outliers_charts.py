import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


DATA_DIR = Path(__file__).resolve().parents[3] / "data"
create_directory(DATA_DIR)


""" ----------------LEITURA DF---------------- """

csv_path = DATA_DIR / 'df_deputados.csv'
csv_path_frente = DATA_DIR / 'membros_frente.csv'

df = pd.read_csv(csv_path)
df_frente = pd.read_csv(csv_path_frente)

df.head()


""" ----------------BOXPLOT DE GASTOS---------------- """

def boxplot_gastos(df):

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()

    # Gráfico de boxplot
    fig = px.box(df_gastos, y="valorLiquido", title='Boxplot de Gastos')
    fig.update_layout(title_x=0.5)
    fig.update_layout(xaxis_tickvals=[], xaxis_title="")
    
    # Retorna o gráfico
    return fig

boxplot_gastos(df)

""" ----------------BOXPLOT DE GASTOS - PARLAMENTAR---------------- """

def boxplot_gastos_parlamentar(df):

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()

    # Gráfico de boxplot
    fig = px.box(df_gastos, y="valorLiquido", x='nome', points="all", title='Gastos por Parlamentar')
    fig.update_layout(title_x=0.5)
    fig.update_layout(xaxis_tickvals=[], xaxis_title="")
    
    # Retorna o gráfico
    return fig

boxplot_gastos_parlamentar(df)



""" ----------------BOXPLOT DE GASTOS - PARTIDO---------------- """

def boxplot_gastos_partido(df):

    # Agrupa os dados por parlamentar, soma os gastos e adiciona a sigla do partido
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()
    df_gastos['siglaPartido'] = df['siglaPartido']

    # Gráfico de boxplot
    fig = px.box(df_gastos, x='siglaPartido', y="valorLiquido", title='Gastos por Partido')    
    fig.update_layout(title_x=0.5)

    # Retorna o gráfico
    return fig

boxplot_gastos_partido(df)

""" ----------------PARLAMENTARES QUE MAIS GASTAM---------------- """

def top_parlamentares_gastos(df, top_n=10):

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()
    df_gastos['siglaPartido'] = df['siglaPartido']

    # Ordena os gastos em ordem decrescente e seleciona os top N
    df_top_gastos = df_gastos.nlargest(top_n, 'valorLiquido')

    # Formata os valores monetários
    df_top_gastos['valorLiquido_fmt'] = df_top_gastos['valorLiquido'].apply(lambda v: f'R${v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

    # Tabela de gastos
    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=['Parlamentar', 'Gasto Total', 'Partido'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[df_top_gastos['nome'], df_top_gastos['valorLiquido_fmt'], df_top_gastos['siglaPartido']],
                fill_color='lavender',
                align='left'
            )
        )]
    )
    
    fig.update_layout(title='Parlamentares com Maior Gasto', title_x=0.5)

    return fig

top_parlamentares_gastos(df)