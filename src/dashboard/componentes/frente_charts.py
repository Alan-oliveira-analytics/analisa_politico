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

df_frente = pd.read_csv(csv_path_frente)



# gráfico 4 - tabela de frentes
def grafico_tabela_frentes(df, politico=None, partido=None):

    # condicionais para a filtragem
    if politico:
        df = df[df['nome'] == politico]
    if partido:
        df = df[df['siglaPartido'] == partido]

    # gráfico vertical
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Nome</b>", "<b>Partido</b>", "<b>Frente Parlamentar</b>", "<b>Cargo</b>"],
        fill_color='#65727a',
        font=dict(color='white'),
        align='left'
    ),
    cells=dict(
        values=[
            df.nome,
            df.siglaPartido,
            df.titulo_frente,
            df.titulo
        ],
        fill_color='#d7dacf',
        align='left'
    )
    )])

    fig.update_layout(title="Frentes Parlamentares que o Candidato Participa", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig
