import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dash import dash_table
from dash import html

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

    columns = [
        {'name': 'Parlamentar', 'id': 'nome'},
        {'name': 'Fornecedor', 'id': 'nomeFornecedor'},
        {'name': 'Valor Líquido', 'id': 'valorLiquido', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
        {'name': 'Nota Fiscal', 'id': 'link_nota', 'presentation': 'markdown'},
        {'name': 'CNPJ', 'id': 'cnpjCpfFornecedor'},
    ]

    style_table = {
        'maxHeight': '400px',
        'overflowY': 'auto',
        'overflowX': 'auto',
        'border': '1px solid white',
    }

    style_cell = {
        'textAlign': 'left',
        'fontSize': '13px',
        'padding': '6px',
        'whiteSpace': 'normal',
        'border': '1px solid white',
    }

    style_cell_conditional = [
        {
            'if': {'column_id': col},
            'minWidth': '100px',
            'maxWidth': '160px',
            'width': '160px',
            'backgroundColor': '#e6e8e3',
        } for col in ['nomeFornecedor', 'nome']
    ] + [
        {
            'if': {'column_id': 'valorLiquido'},
            'textAlign': 'right',
            'backgroundColor': '#e6e8e3',
        },
        {
            'if': {'column_id': 'link_nota'},
            'textAlign': 'center',
            'backgroundColor': '#e6e8e3',
        },
        {
            'if': {'column_id': 'cnpjCpfFornecedor'},
            'backgroundColor': '#e6e8e3',
        }
    ]

    style_data_conditional = [
        {
            'if': {'column_id': 'valorLiquido'},
            'backgroundColor': '#e6e8e3',
        }
    ]

    style_header = {
        'backgroundColor': '#65727a',
        'color': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'border': '1px solid white',
    }

    table = dash_table.DataTable(
        columns=columns,
        data=df.to_dict('records'),
        style_table=style_table,
        fixed_rows={'headers': True},
        style_cell=style_cell,
        style_cell_conditional=style_cell_conditional,
        style_data_conditional=style_data_conditional,
        style_header=style_header,
    )

    return html.Div([
        html.H4("Detalhamento de Despesas", style={'textAlign': 'center', 'marginBottom': '16px'}),
        table
    ])



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
        labels={'valorLiquido': '', 'tipoDespesa': ''},
        color_discrete_sequence=['#65727a']
    )
    #invertendo para mostrar do maior para o menor
    fig = fig.update_yaxes(categoryorder='total ascending')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
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
    # Calcula a média geral e os limites de controle (UCL/LCL)
    media_geral = df_graph_5['valorLiquido'].mean()
    std_geral = df_graph_5['valorLiquido'].std()
    ucl = media_geral + 3 * std_geral
    lcl = max(media_geral - 3 * std_geral, 0)

    # Destaca pontos acima do UCL
    df_graph_5['acima_ucl'] = df_graph_5['valorLiquido'] > ucl

    fig = px.line(
        df_graph_5,
        x='mes',
        y='valorLiquido',
        color='ano',
        title='Gráfico de Controle dos Gastos',
        labels={'valorLiquido': '', 'mes': 'Mês'},
        markers=True,
        text='valorLiquido',
    ).update_yaxes(showticklabels=False)

    # Adiciona linhas de média, UCL e LCL
    fig.add_hline(y=media_geral, line_dash="dash", line_color="#bec3bc", annotation_text="Média", annotation_position="top left")
    fig.add_hline(y=ucl, line_dash="dot", line_color="red", annotation_text="UCL", annotation_position="top left")
    fig.add_hline(y=lcl, line_dash="dot", line_color="orange", annotation_text="LCL", annotation_position="bottom left")

    # Adiciona destaque para pontos acima do UCL
    for _, row in df_graph_5[df_graph_5['acima_ucl']].iterrows():
        fig.add_scatter(
            x=[row['mes']],
            y=[row['valorLiquido']],
            mode='markers',
            marker=dict(color='red', size=12, symbol='star'),
            name='Acima UCL',
            showlegend=False
        )
    fig.update_traces(texttemplate='%{y:.2s}', textposition='top center')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
    return fig



def indicador_gasto_total(df, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]
    
    total_gasto = df['valorLiquido'].sum()

    indicador = go.Figure(go.Indicator(
    mode = "number",
    value = total_gasto,
    title = {"text": "Gasto Total", 'font': {'size': 18}},
    number={'font': {'size': 15}}
    ))

    indicador.update_traces(number={'valueformat': ',.2f', 'prefix': 'R$'})
    
    indicador.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  
    plot_bgcolor='rgba(0,0,0,0)'    
)
    return indicador


def indicador_numero_gastos(df, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]
    
    total_gastos = df.shape[0]

    indicador = go.Figure(go.Indicator(
    mode = "number",
    value = total_gastos,
    title = {"text": "Número de Gastos", 'font': {'size': 18}},
    number={'font': {'size': 15}}
    ))

    indicador.update_traces(number={'valueformat': '.d', 'prefix': ''})
    
    indicador.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  
    plot_bgcolor='rgba(0,0,0,0)')

    return indicador


def ticket_medio_gastos(df, partido=None, politico=None):
    if politico:
        df = df[df['nome'] == politico]

    if partido:
        df = df[df['siglaPartido'] == partido]

    # Ignora valores menores ou iguais a 0
    df = df[df['valorLiquido'] > 0]
    
    total_gastos = df.shape[0]
    total_valor = df['valorLiquido'].sum()

    if total_gastos > 0:
        ticket_medio = total_valor / total_gastos
    else:
        ticket_medio = 0

    indicador = go.Figure(go.Indicator(
    mode = "number",
    value = ticket_medio,
    title = {"text": "Ticket Médio", 'font': {'size': 18}},
    number={'font': {'size': 15}}
    ))

    indicador.update_traces(number={'valueformat': ',.2f', 'prefix': 'R$'})
    
    indicador.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  
    plot_bgcolor='rgba(0,0,0,0)')

    return indicador