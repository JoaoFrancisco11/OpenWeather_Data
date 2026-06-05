import requests
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def extract_weather_data(url:str) -> list:
    """
    Realiza a extração dos dados meteorológicos via requisição HTTP GET.

    Args:
        url (str): Endpoint da API OpenWeather Formatada
    Returns:
        List: Lista contendo os dados brutos da respota ou uma lista vazia em caso de falha.
    """
    
    # ---------------- Requisição
    try:
        response = requests.get(url)

    except requests.exceptions.RequestException as e:
        logging.error(f'Erro na requisição! Status: {response.status_code}')
        logging.error(f'Detalhe do erro: {response.text}')
        return []
    
    # Processamento do corpo da resposta
    data = response.json()

    if not data:
        logging.warning('Requisição retornando dados vazio: {response.status_code}')
        return []
    
    # ---------------- Criando sistema de arquivos para persistência
    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------- salvamento do arquivo em formato JSON
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f'Arquivo salvo em path {output_path}') 
    except IOError as e:
        logging.error(f'Erro ao gravar arquivo em disco: {e}')
        return []
    return data
