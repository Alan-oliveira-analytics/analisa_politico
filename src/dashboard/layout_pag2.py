# Essenciais
import pandas as pd
from pathlib import Path

# Dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Gráficos
from .componentes.indicadores import indicadores
from .componentes.outliers_charts import boxplot_gastos, top_parlamentares_gastos, gerar_interpretador_boxplot, tabela_frequencia


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
csv_path_frente = DATA_DIR / 'membros_frente.csv'

df = pd.read_csv(csv_path)
df_frente = pd.read_csv(csv_path_frente)
df.head()
opcoes_meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

opcoes_ano = df['ano'].unique().tolist()

# Estilo do layout
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '280px',
    'padding': '20px',
    'background-color': '#8f9a9c',
}

content_style = {
    'margin-left': '280px', 
    'padding': '20px',
    'background-color': '#e6e8e3',
    'minHeight': '100vh',
    'boxsizing': 'border-box'
}


def layout_pagina_2():


    return  html.Div([
        #sidebar
        html.Div(
    [
        html.H1(f'Dashboard', style={'font-size': '36px', 'color': '#ffffff', 'textAlign': 'center'}),
        html.Hr(),
        html.P(
            'Análise de gastos de políticos',
            style={'font-size': '20px', 'color': '#ffffff', 'textAlign': 'center'}
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Análise de Gastos", href="/analise-gastos", active="exact"),
                dbc.NavLink("Detecção de Anomalias", href="/deteccao-anomalia", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),

        html.Hr(),
 

        # ---------------------------------FILTROS--------------------------------------       
        html.Div([
            'Escolha o ano:',
            dcc.Dropdown(opcoes_ano, value='Todos', id='drop_ano'),
        ]),

        html.Hr(),
        html.Div([
            'Escolha o mês:',
            dcc.Dropdown(opcoes_meses, value='Todos', id='drop_mes'),
        ]),

    ],
        style=sidebar_style
            ),

    #----------------GRÁFICOS----------------

        # Conteúdo principal    
        html.Div([


        html.Div([


            dcc.Graph(
                id = 'indicador_media',
                figure=indicadores(tipo='media', df=df),
                style={
                'display': 'inline-block',
                'width': '100%',
                'minWidth': '220px',
                'maxWidth': '350px',
                'flex': '1',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            }
            ),

            dcc.Graph(
                id = 'indicador_mediana',
                figure=indicadores(tipo='mediana', df=df),
                style={
                'display': 'inline-block',
                'width': '100%',
                'minWidth': '220px',
                'maxWidth': '350px',
                'flex': '1',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            }
            ),

            dcc.Graph(
                id = 'indicador_deputados_outliers',
                figure=indicadores(tipo='deputados_outliers', df=df),
                style={
                'display': 'inline-block',
                'width': '100%',
                'minWidth': '220px',
                'maxWidth': '350px',
                'flex': '1',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            }
            ),

            dcc.Graph(
                id = 'categoria_mais_gastos',
                figure=indicadores(tipo='categoria_mais_gastos', df=df),
                style={
                'display': 'inline-block',
                'width': '100%',
                'minWidth': '220px',
                'maxWidth': '350px',
                'flex': '1',
                'height': '100px',
                'backgroundColor': '#ffffff',
                'border': '1px solid #dee2e6',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            }
            )

        ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'gap': '20px',
                'marginBottom': '30px'
                  }),


      html.Div([

    # Boxplot gráfico (lado esquerdo)
    html.Div([
        dcc.Graph(
            id='boxplot_gastos_parlamentar',
            figure=boxplot_gastos(df),
            config={'displayModeBar': False},
        )
    ], style={
            'flex': '1',
            'minWidth': '400px',
            'maxWidth': '600px',
            # 'padding': '10px',
            'boxSizing': 'border-box',
            # 'height': '400px'  # altura fixa igual ao card
    }),

    # Resumo estilo card (lado direito)
    html.Div(
        gerar_interpretador_boxplot(df),
        id='interpretador_boxplot',
        style={
            'flex': '1',
            'minWidth': '350px',
            'maxWidth': '600px',
            'backgroundColor': '#ffffff',  # ou '#f8f9fa'
            'border': '1px solid #dee2e6',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            # 'height': '400px',
        }
    )

     ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'alignItems': 'center',
                'gap': '20px',
                'width': '100%',
                'marginBottom': '30px'
        }),


    html.Div([
        tabela_frequencia(df)
    ], id='tabela_frequencia')

    ], style=content_style)
    ])