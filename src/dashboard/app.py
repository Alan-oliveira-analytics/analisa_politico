from dash import Dash, html, dash_table
import pandas as pd

df = pd.read_csv('./data/tb_deputados.csv')


# inicializa o app
app = Dash()

# app layout
app.layout = [
    html.H1(children='Dashboard Análise Políticos'),

    html.Div(children='teste'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

if __name__ == '__main__':
    app.run(debug=True)

