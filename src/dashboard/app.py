from dash import Dash, dcc, html
from .callbacks import registro_callback

import dash_bootstrap_components as dbc

# inicializa o app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# registrar callbacks
registro_callback(app)

# app layout
app.layout = html.Div([
    dcc.Location(id='url'),  # Captura a URL atual
    html.Div(id='page-content')  # Onde o conteúdo será injetado dinamicamente
])


# rodar o app
if __name__ == '__main__':
    app.run(debug=True)

