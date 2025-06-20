import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dash import html, dash_table, dcc
from functions.modulos_analise_dados import tabela_frequencia_bilateral

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

def boxplot_gastos(df, nome_col='nome', mes=None, ano=None, partido=None):

    if mes:
        df = df[df['mes_nome'] == mes]

    if ano:
        df = df[df['ano'] == ano]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby(nome_col)['valorLiquido'].sum().reset_index()

    # boxplot
    fig = go.Figure()
    fig.add_trace(go.Box(y=df_gastos['valorLiquido'],
                         name='Gastos',
                         hovertext=df_gastos[nome_col],
                         marker_color = '#8f9a9c',
                         boxpoints='outliers',
                         boxmean=True,
                         ))
    
    # alterações layout
    fig.update_layout(title='Boxplot de Gastos', 
                      title_x=0.5,
                      xaxis_tickvals=[],
                      xaxis_title=''),
    
    # Retorna o gráfico
    return fig

boxplot_gastos(df)
boxplot_gastos(df, nome_col='siglaPartido')



""" ----------------FUNÇÃO QUE RETORNA O INTERPRETADOR DO BOXPLOT---------------- """

def gerar_interpretador_boxplot(df, nome_col='nome', mes=None, ano=None, partido=None):

    if mes:
        df = df[df['mes_nome'] == mes]

    if ano:
        df = df[df['ano'] == ano]
    
    if partido:
        df = df[df['siglaPartido'] == partido]

    df_gastos = df.groupby(nome_col)['valorLiquido'].sum().reset_index()

    q3 = df_gastos['valorLiquido'].quantile(0.75)
    q1 = df_gastos['valorLiquido'].quantile(0.25)
    iqr = q3 - q1
    limite_superior = q3 + 1.5 * iqr

    outliers = df_gastos[df_gastos['valorLiquido'] > limite_superior]
    
    percentual_outliers = outliers['valorLiquido'].sum() / df_gastos['valorLiquido'].sum() * 100

    interpretador = html.Div([

        html.H4('Resumo do Boxplot'),
        html.P(f'75% dos gastos vão até R${q3:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')),
        html.P(f'Os parlamentares com gastos acima de R${limite_superior:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' são considerados outliers.'),
        html.P(f'Os valores outliers representam {percentual_outliers:.2f}% do total de gastos.')
    ])

    return interpretador



""" ----------------PARLAMENTARES QUE MAIS GASTAM---------------- """

def top_parlamentares_gastos(df, top_n=10):

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()
    df_gastos['siglaPartido'] = df['siglaPartido']

    # Ordena os gastos em ordem decrescente e seleciona os top N
    df_top_gastos = df_gastos.nlargest(top_n, 'valorLiquido')

    # Formata os valores monetários
    df_top_gastos['valorLiquido_fmt'] = df_top_gastos['valorLiquido'].apply(lambda v: f'R${v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

    # Tabela de gastos
    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=['Parlamentar', 'Gasto Total', 'Partido'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[df_top_gastos['nome'], df_top_gastos['valorLiquido_fmt'], df_top_gastos['siglaPartido']],
                fill_color='lavender',
                align='left'
            )
        )]
    )
    
    fig.update_layout(title='Parlamentares com Maior Gasto', title_x=0.5)

    return fig

""" ----------------TABELA DE FREQUÊNCIA BILATERAL---------------- """

def tabela_frequencia(df, mes=None, ano=None):
    if mes:
        df = df[df['mes_nome'] == mes]
    if ano:
        df = df[df['ano'] == ano]


    # Cria a tabela de frequência bilateral
    tabela = tabela_frequencia_bilateral(df, 'siglaPartido', 'valorLiquido', len(df['siglaPartido'].unique())).reset_index()
    
    # Conta quantos parlamentares ativos por partido
    partido_membros = df.groupby('siglaPartido')['nome'].nunique().to_dict()

    # Gera tooltips personalizados
    tooltips = [
        {
            'siglaPartido': {
                'value': f"{partido_membros.get(row['siglaPartido'], 0)} parlamentares em exercício",
                'type': 'text'
            }
        }
        for _, row in tabela.iterrows()
    ]

       # Remove index
    tabela = tabela.drop(columns=['index'], errors='ignore')

    # Renomeia colunas
    tabela = tabela.rename(columns={
        'Percentual sobre o total (%)': '% sobre o total',
        'Percentual acumulado (%)': '% acumulado'
    })

    # Cria tabela Dash
    table_dash = dash_table.DataTable(
        data=tabela.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in tabela.columns],
        tooltip_data=tooltips, 
        tooltip_duration=None,
        style_table={'height': '400px', 'overflowY': 'auto'},
        fixed_rows={'headers': True},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': '#d7dacf', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'}
        ],
        style_cell_conditional=[
            {'if': {'column_id': 'siglaPartido'}, 'width': '10%'},
            {'if': {'column_id': 'Gasto Total (R$)'}, 'width': '10%'}
        ],
    )

    # Embalar no layout
    layout_tabela = html.Div([
        html.H4("Detalhamento de Despesas por Partido", style={'textAlign': 'center', 'marginBottom': '16px'}),
        table_dash
    ])

    return layout_tabela

tabela_frequencia(df)