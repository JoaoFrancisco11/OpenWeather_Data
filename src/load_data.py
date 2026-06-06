from sqlalchemy import create_engine, text # create_engine é para fazer a conexão com o banco e text para escrever código sql
from urllib.parse import quote_plus #usada para codificar strings em um formato seguro para URLs, substituindo espaços por sinais de adição (+) e convertendo caracteres especiais em sequências de escape percentual (ex: %20)
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv # Carregar as variáveis do arquivo .env
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
