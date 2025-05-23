# Essenciais
import pandas as pd
from pathlib import Path

# Dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Gráficos
from .charts import grafico_1, grafico_2, grafico_3, grafico_4, grafico_5, grafico_6


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
csv_path_frente = DATA_DIR / 'membros_frente.csv'

df = pd.read_csv(csv_path)
df_frente = pd.read_csv(csv_path_frente)
# Adicionando a nova coluna com base no espectro político
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

df['espectro_politico'] = df['siglaPartido'].map(espectro_politico)


df.columns

opcoes_espectro = ['Direita', 'Esquerda', 'Centro', 'Centro-direita', 'Centro-esquerda']

opcoes_partido = ['MDB', 'REPUBLICANOS', 'PL', 'PSDB', 'NOVO', 'PP', 'PDT', 'PT',
       'CIDADANIA', 'UNIÃO', 'PCdoB', 'PV', 'AVANTE', 'PSD',
       'SOLIDARIEDADE', 'PSB', 'PODE', 'PSOL', 'PRD', 'REDE']

opcoes_politico = df['nome'].unique().tolist()

# Estilo do layout
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16%',
    'padding': '20px',
    'background-color': '#f8f9fa',
}

content_style = {
    'margin-left': '18rem',
    'padding': '20px',
    'background-color': '#ffffff',
}


def cria_layout():


    return  html.Div([
        #sidebar
        html.Div(
    [
        html.H1(f'Dashboard', style={'font-size': '36px'}),
        html.Hr(),
        html.P(
            'Análise de gastos de políticos',
            style={'font-size': '20px', 'color': '#6c757d'}
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Página 1", href="/pagina-1", active="exact"),
                dbc.NavLink("Página 2", href="/pagina-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),

        html.Hr(),
 
    # ---------------------------------FILTROS--------------------------------------       
        html.Div([
            'Escolha o partido:',
            dcc.Dropdown(opcoes_partido, value='Todos', id='drop_partido'),
        ]),

        html.Hr(),
        html.Div([
            'Escolha o Político:',
            dcc.Dropdown(opcoes_politico, value='Todos', id='drop_politico'),
        ]),

    ],
    style=sidebar_style
    ),
   

    # ---------------------------------GRÁFICOS--------------------------------------
    
    # Conteúdo principal
    html.Div([  # div principal que vai conter o conteúdo


    html.H1(
        children='Dashboard Análise Políticos',
        style={'textAlign': 'center'}
    ),
    
    html.Div([
        dcc.Graph(
        id='grafico_gastos_sazonalidade',
        figure=grafico_5(df),
    )], style={'width': '50%', 'display': 'inline-block'}),

    
    html.Div([
        dcc.Graph(
        id='grafico_frentes_parlamentares',
        figure=grafico_6(df_frente),
    )], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_fornecedor',
        figure=grafico_3(df)
    )], style={'width': '50%', 'display': 'inline-block'}),

  
    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_despesa',
        figure=grafico_4(df)
    )], style={'width': '50%', 'display': 'inline-block'}),



        ])], style=content_style
)