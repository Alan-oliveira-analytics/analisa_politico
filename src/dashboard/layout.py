from dash import html, dcc
from .charts import grafico_1
from .charts import grafico_2
from .charts import grafico_3
from .charts import grafico_4

opcoes_espectro = ['Direita', 'Esquerda', 'Centro', 'Centro-direita', 'Centro-esquerda']

opcoes_partido = ['MDB', 'REPUBLICANOS', 'PL', 'PSDB', 'NOVO', 'PP', 'PDT', 'PT',
       'CIDADANIA', 'UNIÃO', 'PCdoB', 'PV', 'AVANTE', 'PSD',
       'SOLIDARIEDADE', 'PSB', 'PODE', 'PSOL', 'PRD', 'REDE']

def cria_layout():


    return html.Div([
    html.H1(
        children='Dashboard Análise Políticos',
        style={'textAlign': 'center'}
    ),
    

    html.Div([
        dcc.Graph(
        id='grafico_gastos_espectro_politico',
        figure=grafico_1(),
    )], style={'width': '50%', 'display': 'inline-block'}),

    
    html.Div([
        dcc.Graph(
        id='grafico_politicos_por_espectro',
        figure=grafico_2()
    )], style={'width': '50%', 'display': 'inline-block'}),


    html.Div([
        dcc.Dropdown(opcoes_espectro, 'Todos', id='drop_espectro'),
    ], style={'width': '50%', 'display': 'inline-block'}),
    

    html.Div([
        dcc.Dropdown(opcoes_partido, value='Todos', id='drop_partido'),
    ], style={'width': '50%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_fornecedor',
        figure=grafico_3()
    )], style={'width': '50%', 'display': 'inline-block'}),

  
    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_despesa',
        figure=grafico_4()
    )], style={'width': '50%', 'display': 'inline-block'}),
])