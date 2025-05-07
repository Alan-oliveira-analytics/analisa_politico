from dash import html, dcc
from .charts import grafico_1
from .charts import grafico_2

def cria_layout():
    return html.Div([
    html.H1(
        children='Dashboard Análise Políticos',
        style={'textAlign': 'center'}
    ),
    
    dcc.Graph(
        id='grafico_gastos_espectro_politico',
        figure=grafico_1()
    ),

    dcc.Graph(
        id='grafico_politicos_por_espectro',
        figure=grafico_2()
    )
])