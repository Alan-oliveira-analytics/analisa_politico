# Essenciais
import pandas as pd
from pathlib import Path

# Dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Gráficos
from .componentes.gastos_charts import grafico_gastos_fornecedor, grafico_gastos_tipo_despesa, grafico_sazonalidade, indicador_numero_gastos, indicador_gasto_total, ticket_medio_gastos
from .componentes.frente_charts import grafico_tabela_frentes


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

print(type(indicador_gasto_total))
print(type(indicador_numero_gastos))
print(type(ticket_medio_gastos))

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


def layout_pagina_1():


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


    html.Div([

        dcc.Graph(id='indicador_gasto_total', figure=indicador_gasto_total(df), 
                  style={'display': 'inline-block', 'width': '32%', 'marginRight': '2%'}),

        dcc.Graph(id='indicador_numero_gastos', figure=indicador_numero_gastos(df), 
                  style={'display': 'inline-block', 'width': '32%', 'marginRight': '2%'}),

        dcc.Graph(id='ticket_medio_gastos', figure=ticket_medio_gastos(df), 
                  style={'display': 'inline-block', 'width': '32%'})
    ]),
    

    html.Div([
        dcc.Graph(
        id='grafico_gastos_sazonalidade',
        figure=grafico_sazonalidade(df),
    )], style={'width': '50%', 'display': 'inline-block'}),

    
    html.Div([
        dcc.Graph(
        id='grafico_frentes_parlamentares',
        figure=grafico_tabela_frentes(df_frente),
    )], style={
        'width': '50%', 
        'display': 'inline-block',
        'backgroundColor': '#f8f9fa',      
        'border': '1px solid #dee2e6',   
        'borderRadius': '8px',         
        'padding': '20px',                
        'marginBottom': '20px',           
        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)' 
        }),


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