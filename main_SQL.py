import logging
import logfire
import time
from exctract_SQL import *
from logging import basicConfig, getLogger
from dotenv import load_dotenv

load_dotenv()

logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()


if __name__ == '__main__':
    cria_tabela()
    logger.info("tabela criada")

    while True:
        try:
            dados = extract_data_btc()
            if dados:
                dados_tratados = transform_dados_btc(dados)
                load_dados_btc(dados_tratados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("Saindo do programa")
            break
        except Exception as e:
            print("Erro", e)
            time.sleep(15)