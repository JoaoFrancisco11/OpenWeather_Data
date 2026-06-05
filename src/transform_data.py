import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'

def create_datafrme(path_name:str) -> pd.DataFrame:
    logging.info("→ Criando Dataframe do arquivo JSON...")

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        with open(path_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logging.info("→ Normalizando dados JSON para DataFrame...")
        df = pd.json_normalize(data)
        logging.info(f"\n✔ Dataframe criado com {len(df)} linhas!")
        return df

    except IOError as e:
        logging.error(f'Erro ao carregar o arquivo JSON: {e}')
        return pd.DataFrame()