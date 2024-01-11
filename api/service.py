import requests


def get_data(data):
    try:
        url = f'https://cruviana.ifpi.edu.br/oeiras/api/v1/leituras/?Data={data}'
        response = requests.get(url)
        return response.json()['results']
    except:
        requests.exceptions.RequestException()