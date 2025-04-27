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

""" ----------------CONFIGURAÇÃO DE CAMINHO---------------- """
# Caminho da raiz do projeto (dois níveis acima do script atual)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Pasta de dados (dentro da raiz)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(ROOT_DIR, "data")

if not os.path.exists(DATA_DIR):
    print(f"O diretório {DATA_DIR} não existe, criando...")
    os.makedirs(DATA_DIR, exist_ok=True)
else:
    print(f"O diretório {DATA_DIR} já existe.")

# Testando a criação de um arquivo dentro do diretório
try:
    test_file_path = os.path.join(DATA_DIR, "test.txt")
    with open(test_file_path, 'w') as f:
        f.write("Teste de gravação!")
    print(f"Arquivo criado com sucesso: {test_file_path}")
except OSError as e:
    print(f"Erro ao tentar gravar no diretório: {e}")

    
""" ----------------IMPORTAÇÃO CLASSE---------------- """
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.api.deputados_api import deputadoAPI



""" ----------------COLETANDO OS DADOS---------------- """
# instancia api
api = deputadoAPI(base_url='https://dadosabertos.camara.leg.br/api/v2/')

# requisição dos dados - Dimensão Deputados
dados = api.get_dados(endpoint='deputados')
dados = dados['dados']

df = pd.DataFrame(dados)
df.to_csv('./data/tb_deputados.csv', index=False)



# Pegando as informações Gerais dos Deputados
coluna_id = list(df['id'])
deputados_informacoes = {}


for x in coluna_id:
# requisitar os dados
    dados = api.get_dados(endpoint=f'deputados/{x}')
    dados.keys()

    dados = dados['dados']
    deputados_informacoes[dados['id']] = dados

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