from sqlalchemy import create_engine, text # create_engine é para fazer a conexão com o banco e text para escrever código sql
from urllib.parse import quote_plus #usada para codificar strings em um formato seguro para URLs, substituindo espaços por sinais de adição (+) e convertendo caracteres especiais em sequências de escape percentual (ex: %20)
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv # Carregar as variáveis do arquivo .env
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')

host = 'host.docker.internal'

def get_engine():
    logging.info(f"\n ➔ Conectando em {host}:5432/{database}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

def load_database(table_name:str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index = False
    )
    logging.info(f"\n✔ Dados Carregados com Sucesso!")

    df_check = pd.read_sql('SELECT * FROM {table_name}', con=engine)
    logging.info(f"\nTotal de registros na tabela: {len(df_check)}\n")
    return []