from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from .charts import grafico_3, grafico_4, grafico_5, grafico_6
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
csv_path_frente = DATA_DIR / 'membros_frente.csv'

df = pd.read_csv(csv_path)
df_frente = pd.read_csv(csv_path_frente)


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


""" ----------------TODOS OS CALLBACKS---------------- """

def registro_callback(app):

    """Atualiza o gráfico de gastos por fornecedor baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(partido):
        return grafico_3(df, partido=partido)

    """Atualiza o gráfico de gastos por fornecedor baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_fornecedor', 'figure'),
        Input('drop_politico', 'value'),
    )

    def atualizar_grafico_politico(politico):
        return grafico_3(df, politico=politico)
    
    """Atualiza o gráfico de gastos por despesa baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure', allow_duplicate=True),
        Input('drop_partido', 'value'),
        prevent_initial_call=True
    )

    def atualizar_grafico_despesa(partido):
        return grafico_4(df, partido=partido)
    
    """Atualiza o gráfico de gastos por despesa baseado no politico selecionado"""

    @app.callback(
        Output('grafico_gastos_por_despesa', 'figure'),
        Input('drop_politico', 'value'),
    )
    def atualizar_grafico_despesa_politico(politico):
        return grafico_4(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico_sazonalidade(politico):
        return grafico_5(df, politico=politico)
    

    """Atualiza o gráfico de gastos por sazonalidade baseado no partido selecionado"""

    @app.callback(
        Output('grafico_gastos_sazonalidade', 'figure'),
        Input('drop_partido', 'value'),
    )
    def atualizar_grafico_sazonalidade_partido(partido):
        return grafico_5(df, partido=partido)

    """Atualiza o gráfico de frentes parlamentares baseado no político selecionado"""
    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure', allow_duplicate=True),
        Input('drop_politico', 'value'),
        prevent_initial_call=True
    )
    def atualizar_grafico(politico):
        return grafico_6(df_frente, politico=politico)

    """Atualiza o gráfico de frentes parlamentares baseado no partido selecionado"""
    
    @app.callback(
        Output('grafico_frentes_parlamentares', 'figure'),
        Input('drop_partido', 'value')
    )
    def atualizar_grafico(partido):
        return grafico_6(df_frente, partido=partido)


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
    
