# Essenciais
import pandas as pd
from pathlib import Path

# Dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Gráficos
from .componentes.gastos_charts import grafico_gastos_fornecedor, grafico_gastos_tipo_despesa, grafico_sazonalidade
from .componentes.indicadores import indicadores

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
opcoes_meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

opcoes_ano = df['ano'].unique().tolist()

# Estilo do layout
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16%',
    'padding': '20px',
    'background-color': '#8f9a9c',
}

content_style = {
    'margin-left': '16%', 
    'padding': '20px',
    'background-color': '#e6e8e3',
}


def layout_pagina_1():


    return  html.Div([
        #sidebar
        html.Div(
    [
        html.H1(f'Dashboard', style={'font-size': '36px', 'color': '#ffffff', 'textAlign': 'center'}),
        html.Hr(),
        html.P(
            'Análise de gastos de políticos',
            style={'font-size': '20px', 'color': '#ffffff', 'textAlign': 'center'}
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Análise de Gastos", href="/analise-gastos", active="exact"),
                dbc.NavLink("Detecção de Anomalias", href="/deteccao-anomalia", active="exact"),
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
        
        html.Hr(),

        html.Div([
            'Escolha o ano:',
            dcc.Dropdown(opcoes_ano, value='Todos', id='drop_ano'),
        ]),

        html.Hr(),

        html.Div([
            'Escolha o mês:',
            dcc.Dropdown(opcoes_meses, value='Todos', id='drop_mes'),
        ]),

    ],
    style=sidebar_style
    ),
   

    # ---------------------------------GRÁFICOS--------------------------------------
    
    # Conteúdo principal
    html.Div([  # div principal que vai conter o conteúdo


    html.Div([

        dcc.Graph(
            id='indicador_gasto_total',
            figure=indicadores('gasto_total', df),
            style={
                'display': 'inline-block',
                'width': '300px',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            }

        ),

        dcc.Graph(
            id='indicador_numero_gastos',
            figure=indicadores('numero_gastos', df),
            style={
                'display': 'inline-block',
                'width': '300px',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
            }
        ),

        dcc.Graph(
            id='ticket_medio_gastos',
            figure=indicadores('ticket_medio', df),
            style={
                'display': 'inline-block',
                'width': '300px',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
            }
        )
    ],  style={
                'display': 'flex',
                'justifyContent': 'center',    
                'gap': '20px',                 
                'marginBottom': '30px'
    }),
    

    html.Div([
        dcc.Graph(
        id='grafico_gastos_sazonalidade',
        figure=grafico_sazonalidade(df),
    )], style={'width': '100%', 'display': 'inline-block'}),


    html.Div(
        id='grafico_gastos_por_fornecedor',
        children=grafico_gastos_fornecedor(df),   
        style={'width': '100%', 'display': 'inline-block'}),

  
    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_despesa',
        figure=grafico_gastos_tipo_despesa(df)
    )], style={'width': '100%', 'display': 'inline-block'}),



        ])], style=content_style
)