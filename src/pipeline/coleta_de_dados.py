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



# Pegando as informações Gerais dos Deputados
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




# Pegando as informações de despesa
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




















print('Coleta efetuada com sucesso!')