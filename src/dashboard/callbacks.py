from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from .componentes.gastos_charts import grafico_1, grafico_2, grafico_3
from.componentes.frente_charts import grafico_4
from pathlib import Path
from .layout import layout_pagina_1

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


""" ----------------TODOS OS CALLBACKS---------------- """

def registro_callback(app):

    
    # Callback para renderizar páginas conforme a URL
    @app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
    def render_page_content(pathname):
        if pathname == '/pagina-1' or pathname == '/':
            return layout_pagina_1()
        elif pathname == '/pagina-2':
            return html.H1('Conteúdo da Página 2')
        else:
            return html.Div([
                html.H1("404 - Página não encontrada", className='text-danger'),
                html.Hr(),
                html.P(f"A URL {pathname} não existe.")
            ])




    """Atualiza o gráfico de gastos por fornecedor baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(partido):
        return grafico_1(df, partido=partido)




    """Atualiza o gráfico de gastos por fornecedor baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure'),
        Input('drop_politico', 'value'),
    )

    def atualizar_grafico_politico(politico):
        return grafico_1(df, politico=politico)
    
    """Atualiza o gráfico de gastos por despesa baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_grafico_despesa(partido):
        return grafico_2(df, partido=partido)
    
    """Atualiza o gráfico de gastos por despesa baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure'),
        Input('drop_politico', 'value'),
    )
    def atualizar_grafico_despesa_politico(politico):
        return grafico_2(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico_sazonalidade(politico):
        return grafico_3(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure'),
        Input('drop_partido', 'value'),
    )
    def atualizar_grafico_sazonalidade_partido(partido):
        return grafico_3(df, partido=partido)

    """Atualiza o gráfico de frentes parlamentares baseado no político selecionado"""
    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(politico):
        return grafico_4(df_frente, politico=politico)

    """Atualiza o gráfico de frentes parlamentares baseado no partido selecionado"""
    
    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure'),
        Input('drop_partido', 'value')
    )
    def atualizar_grafico(partido):
        return grafico_4(df_frente, partido=partido)


    """Atualiza as opções do dropdown de políticos baseado no partido selecionado"""

    @app.callback(
        Output('drop_politico', 'options'),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )
    def atualizar_opcoes_politico(partido):
        if partido == 'Todos' or partido is None:
            opcoes_politico = [{'label': i, 'value': i} for i in df['nome'].unique()]

        else:
            opcoes_politico = [{'label': i, 'value': i} for i in df[df['siglaPartido'] == partido]['nome'].unique()]
        
        return opcoes_politico
    

    """Atualiza as opções do dropdown de partidos baseado no político selecionado"""

    @app.callback(
        Output('drop_partido', 'options'),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )


    def atualizar_opcoes_partido(politico):
        if politico == 'Todos' or politico is None:
            opacoes_partido = [{'label': i, 'value': i} for i in df['siglaPartido'].unique()]

        else:
            opacoes_partido = [{'label': i, 'value': i} for i in df[df['nome'] == politico]['siglaPartido'].unique()]
        
        return opacoes_partido
    


