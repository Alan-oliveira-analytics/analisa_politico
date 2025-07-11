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


"""" ----------------FUNÇÕES---------------- """

def calcular_gasto_total(df):

    return df['valorLiquido'].sum()

def calcular_numero_gastos(df):

    return df['valorLiquido'].count()

def calcular_ticket_medio(df):
    if df['valorLiquido'].count() == 0:
        return 0
    return df['valorLiquido'].sum() / df['valorLiquido'].count()


def calcular_media(df):

    return df['valorLiquido'].mean()


def calcular_mediana(df):

    return df['valorLiquido'].median()


def calcular_deputados_outliers(df):

    # Agrupa os dados por parlamentar e soma os gastos
    df_gastos = df.groupby('nome')['valorLiquido'].sum().reset_index()

    # Calcula o limite superior para identificar outliers
    q1 = df_gastos['valorLiquido'].quantile(0.25)
    q3 = df_gastos['valorLiquido'].quantile(0.75)
    iqr = q3 - q1
    limite_superior = q3 + 1.5 * iqr

    # Filtra os parlamentares que estão acima do limite superior
    outliers = df_gastos[df_gastos['valorLiquido'] > limite_superior]

    return len(outliers)


def calcular_categoria_mais_gastos(df, ano=None, mes=None):

    if mes:
        df = df[df['mes_nome'] == mes]

    if ano:
        df = df[df['ano'] == ano]

    # Agrupa os dados por categoria e soma os gastos
    df_categoria = df.groupby('tipoDespesa')['valorLiquido'].sum().reset_index()

    # Ordena os gastos em ordem decrescente e seleciona a categoria com maior gasto
    categoria_mais_gastos = df_categoria.nlargest(1, 'valorLiquido')
    return categoria_mais_gastos['valorLiquido'].values[0], categoria_mais_gastos['tipoDespesa'].values[0]


""" ----------------GERAR INDICADOR---------------- """


def gerar_indicador(titulo, valor, prefixo='', valor_formatado=',.2f'):
    
    indicador = go.Figure(go.Indicator(
            mode="number",
            value=valor,
            title={"text": titulo, 'font': {'size': 14}},
            number={'prefix': prefixo, 'valueformat': valor_formatado, 'font': {'size': 15}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
    
    indicador.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  
    plot_bgcolor='rgba(0,0,0,0)')

    return indicador

""" ----------------INDICADORES---------------- """


def indicadores(tipo, df, ano=None, mes=None, politico=None, partido=None):

    # filtros para o callback
    if mes:
        df = df[df['mes_nome'] == mes]

    if ano:
        df = df[df['ano'] == ano]

    if politico:
        df = df[df['nome'] == politico]

    if partido:
        df = df[df['siglaPartido'] == partido]


    if tipo=="media":
        return gerar_indicador(
            titulo="Média de Gastos",
            valor=calcular_media(df),
            prefixo='R$',
            valor_formatado=',.2f'
        )
    
    elif tipo=="mediana":
        return gerar_indicador(
            titulo="Mediana de Gastos",
            valor=calcular_mediana(df),
            prefixo='R$',
            valor_formatado=',.2f'
        )
    
    elif tipo=="deputados_outliers":
        return gerar_indicador(
            titulo="Número de Parlamentares Outliers",
            valor=calcular_deputados_outliers(df),
            valor_formatado=',d'
        )
    
    elif tipo=="categoria_mais_gastos":
        valor, categoria = calcular_categoria_mais_gastos(df)
        return gerar_indicador(
            titulo=f"Categoria com Mais Gastos:<br>{categoria}",
            valor=valor,
            prefixo='R$',
            valor_formatado=',.2f'
        )
    
    elif tipo=="gasto_total":
        return gerar_indicador(
            titulo="Gasto Total",
            valor=calcular_gasto_total(df),
            prefixo='R$',
            valor_formatado=',.2f'  
        )
    
    elif tipo=="numero_gastos":
        return gerar_indicador(
            titulo="Número de Gastos",
            valor=calcular_numero_gastos(df),
            valor_formatado=',d'
        )
    
    elif tipo=="ticket_medio":
        return gerar_indicador(
            titulo="Ticket Médio",
            valor=calcular_ticket_medio(df),
            prefixo='R$',
            valor_formatado=',.2f'
        )