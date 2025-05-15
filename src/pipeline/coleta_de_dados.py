"""
Este script coleta dados de deputados utilizando a API da Câmara dos Deputados
e salva as informações em arquivos CSV para análise posterior.
"""


""" ----------------IMPORTAÇÃO BIBLIOTECAS---------------- """
import pandas as pd
import numpy as np

import requests

import sys
import os
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


    
""" ----------------IMPORTAÇÃO CLASSE---------------- """
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.api.deputados_api import deputadoAPI



""" ----------------COLETANDO OS DADOS---------------- """
# instancia api
api = deputadoAPI(base_url='https://dadosabertos.camara.leg.br/api/v2/')

# requisição dos dados - Dimensão Deputados
data = api.get_dados(endpoint='deputados')
data = data['dados']

df = pd.DataFrame(data)
df.to_csv('./data/tb_deputados.csv', index=False)



""" ----------------INFORMAÇÕES GERAIS DOS DEPUTADOS---------------- """
coluna_id = list(df['id'])
deputados_informacoes = {}

for x in coluna_id:
# requisitar os dados
    data = api.get_dados(endpoint=f'deputados/{x}')
    data.keys()

    data = data['dados']
    deputados_informacoes[data['id']] = data

deputados_informacoes = pd.DataFrame(deputados_informacoes)
deputados_informacoes = deputados_informacoes.T

deputados_informacoes.head()

deputados_informacoes.reset_index(drop=True, inplace=True)
deputados_informacoes = deputados_informacoes.drop(columns=['uri','ultimoStatus', 'urlWebsite', 'redeSocial', 'dataFalecimento'])
deputados_informacoes.head()

deputados_informacoes.to_csv('./data/info_deputados.csv')




""" ----------------INFORMAÇÕES DE DESPESA---------------- """
despesas_deputados = {}
for x in coluna_id:
    # requisitar os dados
    dados = api.get_dados(endpoint=f'deputados/{x}/despesas')
    dados = dados['dados']
    despesas_deputados[x] = dados  # Use 'x' (deputy ID) as the key


# Inicializar uma lista para armazenar os DataFrames gerados
df_list = []

# Iterar sobre cada índice do dicionário
for index, records in despesas_deputados.items():
    # Expandir cada lista de dicionários para um DataFrame
    df_temp = pd.json_normalize(records)
    
    # Adicionar uma coluna com o índice atual
    df_temp['indice'] = index
    
    # Adicionar o DataFrame à lista
    df_list.append(df_temp)

# Concatenar todos os DataFrames na lista em um único DataFrame
df_final = pd.concat(df_list, ignore_index=True)

df_final.head()
df_final.shape


df_final.to_csv('./data/despesas_deputados.csv')


""" ------------------COLETANDO OS DADOS DE PROPOSIÇÕES---------------- """ 
params = {
    'dataInicio': '2025-01-01',
    'dataFim': '2025-03-31',
}

# requisição dos dados - Proposições
proposicoes = api.get_dados(endpoint='proposicoes')
proposicoes = proposicoes['dados']
proposicoes = pd.DataFrame(proposicoes)
proposicoes


""" ------------------COLETANDO OS DADOS DE VOTAÇÃO---------------- """ 

# requisição dos dados - votação
votacoes_org = api.get_dados(endpoint='votacoes', params=params)
votacoes_org = votacoes_org['dados']
votacoes_org = pd.DataFrame(votacoes_org)
votacoes_org.head()
id_votacoes = list(votacoes_org['id'])
id_votacoes

""" ------------------ DETALHANDO VOTAÇÃO---------------- """ 

votacoes_informacoes = pd.DataFrame()
for x in id_votacoes:
    # requisitar os dados
    votacoes = api.get_dados(endpoint=f'votacoes/{x}/votos')
    votacoes = votacoes['dados']
    votacoes = pd.DataFrame(votacoes)
    votacoes['id_votacao'] = x

    # Verifica se a coluna 'deputado_' existe antes de expandir
    if 'deputado_' not in votacoes.columns:
        continue
    else:
        # Expande os valores da coluna 'deputado' em colunas separadas
        deputado_df = pd.json_normalize(votacoes['deputado_'])
        # Remove a coluna 'deputado' original e concatena as novas colunas
        votacoes = pd.concat([votacoes.drop(columns=['deputado_']), deputado_df], axis=1)
        
        votacoes_informacoes = pd.concat([votacoes_informacoes, votacoes], ignore_index=True)       

votacoes_informacoes.to_csv('./data/votacoes_informacoes.csv', index=False)





print('Coleta efetuada com sucesso!')