import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dash import dash_table

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

df_frente.head()



df.head()
# criando uma variável que comporta id's únicos
df_unique_id = df.sort_values(['id']).drop_duplicates('id', keep='first')


# top 10 gastos por fornecedor
def grafico_gastos_fornecedor(df, partido=None, politico=None):

    if politico:
        df = df[df['nome'] == politico]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]

    # Cria links clicáveis para a coluna 'Nota fiscal'
    df['link_nota'] = df['urlDocumento'].apply(
        lambda url: f'[Ver Nota]({url})' if pd.notnull(url) else ''
    )

    df = df.sort_values('valorLiquido', ascending=False)

    fig = dash_table.DataTable(
        columns=[
            {'name': 'Parlamentar', 'id': 'nome'},
            {'name': 'Fornecedor', 'id': 'nomeFornecedor'},
            {'name': 'Valor Líquido', 'id': 'valorLiquido', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
            {'name': 'Nota Fiscal', 'id': 'link_nota', 'presentation': 'markdown'},
            {'name': 'CNPJ', 'id': 'cnpjCpfFornecedor'},
          
        ],
        data=df.to_dict('records'),
            style_table={
                'maxHeight': '400px',   # limita altura e ativa scroll vertical
                'overflowY': 'auto',
                'overflowX': 'auto',    # scroll horizontal se precisar
                'border': '1px solid lightgray',
    },
            style_cell={
                'textAlign': 'left',
                'fontSize': '13px',
                'padding': '6px',
                'whiteSpace': 'normal',
    },
            style_cell_conditional=[
            {
                'if': {'column_id': 'nomeFornecedor', 'column_id': 'nome'},
                'minWidth': '100px',
                'maxWidth': '160px',
                'width': '160px',
        },
        {
                'if': {'column_id': 'valorLiquido'},
                'textAlign': 'right'
        },
        {
                'if': {'column_id': 'link_nota'},
                'textAlign': 'center'
        }
    ],
            style_header={
                'backgroundColor': '#0074D9',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
    },
          
    )
    return fig



# top 10 gastos por tipo de despesa
def grafico_gastos_tipo_despesa(df, espectro=None, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]

    if espectro:
        df = df[df['espectro_politico'] == espectro]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]
    df_graph_3 = df.groupby(['tipoDespesa'])['valorLiquido'].sum().nlargest(10).reset_index()
    df_graph_3['valorLiquido_fmt'] = df_graph_3['valorLiquido'].apply(lambda v: f'R${v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))


    fig = px.bar(
        df_graph_3,
        x='valorLiquido',
        y='tipoDespesa',
        title='TOP 10 - Gastos por Tipo de Despesa',
        text='valorLiquido_fmt',
        orientation='h',
        labels={'valorLiquido': '', 'tipoDespesa': ''}
    )
    #invertendo para mostrar do maior para o menor
    fig = fig.update_yaxes(categoryorder='total ascending')

    return fig


# gráfico 5 - Sazonalidadee
def grafico_sazonalidade(df, espectro=None, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]
    if espectro:
        df = df[df['espectro_politico'] == espectro]
    if partido:
        df = df[df['siglaPartido'] == partido]
    
    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]
    df['ano'] = pd.to_datetime(df['dataDocumento']).dt.year
    df['mes'] = pd.to_datetime(df['dataDocumento']).dt.month
    df["mes"] = df["mes"].astype(str)
    df_graph_5 = df.groupby(['ano', 'mes'])['valorLiquido'].sum().reset_index()

    fig = px.line(
        df_graph_5,
        x='mes',
        y='valorLiquido',
        color='ano',
        title='Sazonalidade dos Gastos',
        labels={'valorLiquido': '', 'mes': 'Mês'},
        markers=True,
        text='valorLiquido',
        ).update_yaxes(showticklabels=False)
        
    fig.update_traces(texttemplate='%{y:.2s}', textposition='top center')
    fig.update_layout(margin=dict(t=60, b=60))
    return fig

