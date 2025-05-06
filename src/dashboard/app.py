from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas as pd
from pathlib import Path



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
df = pd.read_csv(csv_path)
df.head()



""" ----------------DADOS---------------- """
espectro_politico = {
    'PL': 'Centro-direita',
    'PT': 'Esquerda',
    'UNIÃO': 'Centro-direita',
    'PP': 'Centro-direita',
    'REPUBLICANOS': 'Direita',
    'PSD': 'Centro',
    'MDB': 'Centro',
    'PDT': 'Centro-esquerda',
    'PODE': 'Centro-direita',
    'PSB': 'Centro-esquerda',
    'PSOL': 'Esquerda',
    'PSDB': 'Centro',
    'PCdoB': 'Esquerda',
    'AVANTE': 'Centro',
    'PV': 'Centro-esquerda',
    'NOVO': 'Direita',
    'PRD': 'Direita',
    'CIDADANIA': 'Centro-esquerda',
    'SOLIDARIEDADE': 'Centro-esquerda',
    'REDE': 'Centro-esquerda'
}

# Adicionando a nova coluna com base no espectro político
df['espectro_politico'] = df['siglaPartido'].map(espectro_politico)


# inicializa o app
app = Dash()


# criando o grafico
fig = px.bar(df, x='siglaPartido', y='valorLiquido', text_auto='.2s')
fig.show()


# app layout
app.layout = html.Div([
    html.H1(children='Dashboard Análise Políticos'),

    html.Div(children='teste'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])











if __name__ == '__main__':
    app.run(debug=True)

