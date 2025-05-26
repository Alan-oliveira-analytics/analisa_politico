# Essenciais
import pandas as pd
from pathlib import Path

# Dash
from dash import html, dcc
import dash_bootstrap_components as dbc




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

opcoes_partido =df['siglaPartido'].unique().tolist()
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


def layout_pagina_2():


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
        # Conteúdo principal    
        html.Div([
            html.H1("Frentes Parlamentares", className='text-center'),
            html.Hr(),
            dcc.Graph(id='grafico_frentes', figure={}, style={'height': '100vh'}),


        ])], style=content_style
)