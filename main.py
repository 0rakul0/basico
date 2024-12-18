import time
# from exctract_noSQL import *
from exctract_SQL import *

while True:
    dados = extract_data_btc()
    dados_tratados = transform_dados_btc(dados)
    load_dados_btc(dados_tratados, name_db='btc_etl.json')
    time.sleep(15)
