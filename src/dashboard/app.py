from dash import Dash
from .layout import cria_layout


# inicializa o app
app = Dash()

# app layout
app.layout = cria_layout()
       

if __name__ == '__main__':
    app.run(debug=True)

