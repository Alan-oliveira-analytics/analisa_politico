from dash import Dash
from .layout import cria_layout
from .callbacks import registro_callback

import dash_bootstrap_components as dbc

# inicializa o app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app layout
app.layout = cria_layout()

# registrar callbacks
registro_callback(app)

# rodar o app
if __name__ == '__main__':
    app.run(debug=True)

