from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from pathlib import Path

# Importa os componentes do Dash
from .componentes.gastos_charts import grafico_sazonalidade, grafico_gastos_fornecedor, grafico_gastos_tipo_despesa, indicador_gasto_total, indicador_numero_gastos, ticket_medio_gastos

from .componentes.outliers_charts import boxplot_gastos, top_parlamentares_gastos, gerar_interpretador_boxplot, tabela_frequencia

from .componentes.frente_charts import grafico_tabela_frentes

from .componentes.indicadores import indicadores, calcular_categoria_mais_gastos

# Importa o layout das páginas
from .layout import layout_pagina_1
from .layout_pag2 import layout_pagina_2


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
        if pathname == '/analise-gastos' or pathname == '/':
            return layout_pagina_1()
        elif pathname == '/deteccao-anomalia':
            return layout_pagina_2()
        else:
            return html.Div([
                html.H1("404 - Página não encontrada", className='text-danger'),
                html.Hr(),
                html.P(f"A URL {pathname} não existe.")
            ])




    """Atualiza o gráfico de gastos por fornecedor baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'children', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(partido):
        return grafico_gastos_fornecedor(df, partido=partido)


    """Atualiza o gráfico de gastos por fornecedor baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'children'),
        Input('drop_politico', 'value'),
    )
    
    def atualizar_grafico_politico(politico):
        return grafico_gastos_fornecedor(df, politico=politico)
    

    """Atualiza o gráfico de gastos por despesa baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_grafico_despesa(partido):
        return grafico_gastos_tipo_despesa(df, partido=partido)
    
    
    """Atualiza o gráfico de gastos por despesa baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure'),
        Input('drop_politico', 'value'),
    )
    def atualizar_grafico_despesa_politico(politico):
        return grafico_gastos_tipo_despesa(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    
    def atualizar_grafico_sazonalidade(politico):
        return grafico_sazonalidade(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure'),
        Input('drop_partido', 'value'),
    )
    
    def atualizar_grafico_sazonalidade_partido(partido):
        return grafico_sazonalidade(df, partido=partido)


    """Atualiza o gráfico de gastos por sazonalidade baseado no periodo selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure', allow_duplicate=True),
        Input('drop_ano', 'value'),
        prevent_initial_call=True
    )
    
    def atualizar_grafico_sazonalidade_periodo(ano):
        return grafico_sazonalidade(df, ano=ano)


    """Atualiza o gráfico de frentes parlamentares baseado no político selecionado"""

    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    
    def atualizar_grafico(politico):
        return grafico_tabela_frentes(df_frente, politico=politico)

    """Atualiza o gráfico de frentes parlamentares baseado no partido selecionado"""
    
    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure'),
        Input('drop_partido', 'value')
    )
    
    def atualizar_grafico(partido):
        return grafico_tabela_frentes(df_frente, partido=partido)


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
    

    """Atualiza o indicador de gasto total baseado no politico selecionado"""

    @app.callback(
        Output('indicador_gasto_total', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )

    def atualizar_indicador_gasto_total(politico):
        return indicador_gasto_total(df, politico=politico)
    

    """Atualiza o indicador de numero de gastos baseado no politico selecionado"""

    @app.callback(
        Output('indicador_numero_gastos', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )

    def atualizar_indicador_numero_gastos(politico):
        return indicador_numero_gastos(df, politico=politico)
    

    """Atualiza o indicador ticket médio baseado no politico selecionado"""

    @app.callback(
        Output('ticket_medio_gastos', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )

    def atualizar_ticket_medio_gastos(politico):
        return ticket_medio_gastos(df, politico=politico)
    

    """Atualiza o indicador de gasto total baseado no partido selecionado"""

    @app.callback(
        Output('indicador_gasto_total', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_indicador_gasto_total(partido):
        return indicador_gasto_total(df, partido=partido)
    

    """Atualiza o indicador de numero de gastos baseado no partido selecionado"""

    @app.callback(
        Output('indicador_numero_gastos', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_indicador_numero_gastos(partido):
        return indicador_numero_gastos(df, partido=partido)
    

    """Atualiza o indicador ticket médio baseado no partido selecionado"""

    @app.callback(
        Output('ticket_medio_gastos', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_ticket_medio_gastos(partido):
        return ticket_medio_gastos(df, partido=partido)
    
    
    """Função para gerar callback dos indicadores baseado no ano/mes selecionado"""
    
    def gerar_callback_indicador(output_id, tipo, df):
        @app.callback(
            Output(output_id, 'figure', allow_duplicate=True),
            Input('drop_mes', 'value'),
            Input('drop_ano', 'value'),
            prevent_initial_call=True
        )

        def atualizar_indicador(mes, ano):
            
            # Monta um dicionário de filtros
            filtros = {}

            if ano is not None:
                filtros['ano'] = ano
            
            if mes is not None:
                filtros['mes'] = mes

            # Chama a função indicadores com os filtros corretos
            return indicadores(tipo, df, **filtros)
            
    # atualizar indicador média
    gerar_callback_indicador('indicador_media', 'media', df)
    
    # atualizar indicador mediana
    gerar_callback_indicador('indicador_mediana', 'mediana', df)

    # atualizar indicador deputados outliers
    gerar_callback_indicador('indicador_deputados_outliers', 'deputados_outliers', df)

    # atualizar indicador categoria mais gastos
    gerar_callback_indicador('categoria_mais_gastos', 'categoria_mais_gastos', df)


    """Callback texto interpretativo interativo do boxplot"""

    @app.callback(
        Output('interpretador_boxplot', 'children', allow_duplicate=True),
        Input('drop_mes', 'value'),
        Input('drop_ano', 'value'),
        prevent_initial_call=True
        )

    def atualizar_interpretador(mes, ano):

        # Monta um dicionário de filtros
        filtros = {}

        if mes is not None:
            filtros['mes'] = mes

        if ano is not None:
            filtros['ano'] = ano
            
        # Chama a função gerar interpretador boxplot com os filtros corretos
        return gerar_interpretador_boxplot(df, **filtros)
        

    """Callback para o boxplot de gastos"""

    @app.callback(
        Output('boxplot_gastos_parlamentar', 'figure', allow_duplicate=True),
        Input('drop_mes', 'value'),
        Input('drop_ano', 'value'),
        prevent_initial_call=True
    )
    def atualizar_boxplot(mes, ano):
        # Monta um dicionário de filtros
        filtros = {}

        if mes is not None:
            filtros['mes'] = mes

        if ano is not None:
            filtros['ano'] = ano
            
        # Chama a função boxplot_gastos com os filtros corretos
        return boxplot_gastos(df, **filtros)
    
    
    """Callback para a tabela de frequência"""

    @app.callback(
        Output('tabela_frequencia', 'children', allow_duplicate=True),
        Input('drop_mes', 'value'),
        Input('drop_ano', 'value'),
        prevent_initial_call=True
    )
    def atualizar_tabela_frequencia(mes, ano):
        # Monta um dicionário de filtros
        filtros = {}

        if mes is not None:
            filtros['mes'] = mes

        if ano is not None:
            filtros['ano'] = ano
            
        # Chama a função tabela_frequencia com os filtros corretos
        return tabela_frequencia(df, **filtros)
    

    