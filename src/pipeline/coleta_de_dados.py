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
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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
# df.to_csv('./data/tb_deputados.csv', index=False)



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

coluna_id = [204379, 220714, 221328]
# Pegando as informações de despesa
despesas_deputados = {}
for x in coluna_id:
    # requisitar os dados
    dados = api.get_dados(endpoint=f'deputados/{x}/despesas')
    dados = dados['dados']
    despesas_deputados[x] = dados  # Use 'x' (deputy ID) as the key
print(despesas_deputados)

despesas_deputados = pd.DataFrame(despesas_deputados)
# despesas_deputados = despesas_deputados.T
# despesas_deputados.reset_index(drop=True, inplace=True)
print(despesas_deputados)
despesas_deputados.to_csv('./data/info_despesas.csv')






























print('Coleta efetuada com sucesso!')