from datetime import datetime
from pprint import pprint
import requests
import json
from tinydb import TinyDB


#%% extração
def extract_data_btc():
    url = 'https://api.coinbase.com/v2/prices/spot'
    headers = {'Accepts': 'application/json',
               'Content-Type': 'application/json',
               'User-Agent': 'MinhaAplicacao/1.0'}
    params = {"currency": "USD"}
    resp = requests.get(url, headers=headers, params=params)
    return resp.json()

#%% tratamento
def  transform_dados_btc(dados):
    valor = dados['data']['amount']
    cripto = dados['data']['base']
    moeda = dados['data']['currency']
    timestamp = datetime.now().timestamp()

    dados_tratados = {
        'valor': valor,
        'cripto': cripto,
        'moeda': moeda,
        'timestamp': timestamp
    }
    return dados_tratados

#%% load
def load_dados_btc(dados_tratados, name_db):
    db = TinyDB(name_db)
    db.insert(dados_tratados)
    print("dados salvos com sucesso")

if __name__ == '__main__':
    dados = extract_data_btc()
    dados_tratados = transform_dados_btc(dados)
    load_dados_btc(dados_tratados, name_db='btc_etl.json')
