import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


DATA_DIR = Path(__file__).resolve().parents[3] / "data"
create_directory(DATA_DIR)


""" ----------------LEITURA DF---------------- """

csv_path = DATA_DIR / 'df_deputados.csv'
csv_path_frente = DATA_DIR / 'membros_frente.csv'

df = pd.read_csv(csv_path)
df_frente = pd.read_csv(csv_path_frente)

df.head()

""" ----------------BOXPLOT DE GASTOS---------------- """
df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()
df_gastos['siglaPartido'] = df['siglaPartido']
df_gastos
fig = px.box(df_gastos, y="valorLiquido", points="all")
fig.update_layout(xaxis_tickvals=[], xaxis_title="")
fig.show()


""" ----------------BOXPLOT DE GASTOS - PARTIDO---------------- """

fig = px.box(df_gastos, x='siglaPartido', y="valorLiquido")
fig.show()

