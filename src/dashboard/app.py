from dash import Dash
from .layout import cria_layout
from .callbacks import registro_callback

# inicializa o app
app = Dash()

# app layout
app.layout = cria_layout()

# registrar callbacks
registro_callback(app)

# rodar o app
if __name__ == '__main__':
    app.run(debug=True)

