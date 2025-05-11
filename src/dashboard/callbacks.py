from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from .charts import grafico_3
from .charts import grafico_4
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



def registro_callback(app):
    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure', allow_duplicate=True),
        Input('drop_espectro', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(espectro):
        return grafico_3(df, espectro=espectro)


    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure'),
        Input('drop_partido', 'value'),
        
    )

    def atualizar_grafico_partido(partido):
        return grafico_3(df, partido=partido)
    

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure'),
        Input('drop_partido', 'value'),
    )

    def atualizar_grafico_despesa(partido):
        return grafico_4(df, partido=partido)