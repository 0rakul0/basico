from datetime import datetime
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from model_btc import Base, ModelBTC

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

#%% cria o engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def cria_tabela():
    Base.metadata.create_all(engine)

def extract_data_btc():
    url = 'https://api.coinbase.com/v2/prices/spot'
    resp = requests.get(url)
    return resp.json()

#%% tratamento
def  transform_dados_btc(dados):
    valor = dados['data']['amount']
    cripto = dados['data']['base']
    moeda = dados['data']['currency']
    timestamp = datetime.now()

    dados_tratados = {
        'valor': valor,
        'criptomoeda': cripto,
        'moeda': moeda,
        'timestamp': timestamp
    }
    return dados_tratados

#%% load
def load_dados_btc(dados_tratados):
    session = Session()
    novo_registro = ModelBTC(**dados_tratados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados_tratados['timestamp']}] Dados inseridos com sucesso!")