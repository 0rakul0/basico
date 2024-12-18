import psycopg2
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def ler_dados():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )

        query = "SELECT * FROM btc_precos ORDER BY timestamp DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error("Erro ao conectar com o postgres na base de dados")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Dashboard de preços do BTC", layout="wide")
    df = ler_dados()
    if not df.empty:
        st.subheader("DADOS RECENTES")
        st.dataframe(df)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by=['timestamp'])

        st.subheader("Evolução do proço")
        st.line_chart(data=df, x='timestamp', y='valor', use_container_width=True)

        st.subheader("Estatisticas gerais")
        col1, col2, col3 = st.columns(3)
        col1.metric(f"preco atual", f"R$ {df['valor'].iloc[-1]:,.2f}")
        col2.metric(f"preco maximo", f"R$ {df['valor'].max():,.2f}")
        col3.metric(f"preco minimo", f"R$ {df['valor'].min():,.2f}")
    else:
        st.warning("Erro ao puxar os dados")

if __name__ == "__main__":
    main()