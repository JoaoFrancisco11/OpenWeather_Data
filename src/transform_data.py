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

def normalize_weather_column(df:pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0])) 

    df_weather = df_weather.rename(columns={
        'id':'weather_id',
        'main':'weather_main',
        'description':'weather_description',
        'icon':'weather_icon'
    })

    df = pd.concat(df, df_weather, axis=1)

    logging.info(f"\n✔ Coluna 'weather' normalizada - {len(df.columns)} colunas") 

    return df


def drop_columns():
    return pd.DataFrame

def rename_columns():
    return pd.DataFrame