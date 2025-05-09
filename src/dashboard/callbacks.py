from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from .app import app
from .charts import grafico_3

def registro_callback(app):
    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure'),
        Input('drop_espectro', 'value')
    )
    def atualizar_grafico(graf):
        fig = ''


        return fig
    

