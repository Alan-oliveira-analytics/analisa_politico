from dash import html, dcc
import pandas as pd
from pathlib import Path
from .charts import grafico_1
from .charts import grafico_2
from .charts import grafico_3
from .charts import grafico_4

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

# Adicionando a nova coluna com base no espectro político
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

df['espectro_politico'] = df['siglaPartido'].map(espectro_politico)


df.columns

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
        'Filtre por espectro político:',
        dcc.Dropdown(opcoes_espectro, 'Todos', id='drop_espectro'),
    ], style={'width': '50%', 'display': 'inline-block'}),


    html.Div([
        'Filtre por partido:',
        dcc.Dropdown(opcoes_partido, value='Todos', id='drop_partido'),
    ], style={'width': '50%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_fornecedor',
        figure=grafico_3(df)
    )], style={'width': '50%', 'display': 'inline-block'}),

  
    html.Div([
        dcc.Graph(
        id='grafico_gastos_por_despesa',
        figure=grafico_4(df)
    )], style={'width': '50%', 'display': 'inline-block'}),
])