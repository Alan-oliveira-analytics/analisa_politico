from dash import html, dcc
from .charts import grafico_1
from .charts import grafico_2
from .charts import grafico_3

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
        dcc.Graph(
        id='grafico_gastos_por_fornecedor',
        figure=grafico_3()
    )], style={'width': '50%', 'display': 'inline-block'}),


])