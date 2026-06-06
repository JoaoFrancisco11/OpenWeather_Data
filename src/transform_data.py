import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).resolve().parent.parent / 'data' / 'weather_data.json'

columns_name_to_drop = ['weather', 'weather_icon', 'sys.type']

columns_names_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset"
    # weather_id, weather_main, weather_description -> estão no dataframe, mas não vai ser necessário renomear.
}

columns_to_normalize_datetime=['datetime','sunrise','sunset']

def create_datafrme(path_name:str) -> pd.DataFrame:
    logging.info("→ Criando Dataframe do arquivo JSON...")

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        with open(path_name, 'r') as f:
            data = json.load(f)

        logging.info("→ Normalizando dados JSON para DataFrame...")
        df = pd.json_normalize(data)
        logging.info(f'✔ Dataframe criado com {len(df)} linhas!')
       
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

    df = pd.concat([df, df_weather], axis=1)

    logging.info(f"✔ Coluna 'weather' normalizada - {len(df.columns)} colunas") 

    return df

def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f"✔ Removendo colunas: {columns_name}") 
    df = df.drop(columns=columns_name)
    logging.info(f"✔ Colunas removidas: {columns_name}") 
    return df

def rename_columns(df: pd.DataFrame, columns_name:dict[str, str]) -> pd.DataFrame:
    logging.info(f"✔ Renomeado {len(columns_name)} colunas") 
    df = df.rename(columns=columns_name)
    logging.info(f"✔ Colunas renomeadas")    
    return df

def normalize_datetime_columns(df:pd.DataFrame, columns_name:list[str]) -> pd.DataFrame:
    logging.info(f"✔ Convertendo colunas para datetime: {columns_name}")
    for name in columns_name:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo') 
    logging.info(f"✔ Colunas convertidas para datetime: {len(columns_name)}")
    return df


def data_transformations():
    print('\n Iniciando as transformações')

    df = create_datafrme(path_name)
    df = normalize_weather_column(df)
    df = drop_columns(df, columns_name_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)

    logging.info(f"✔ Transformações Concluídas!")

    return df