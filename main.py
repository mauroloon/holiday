import requests

from typing import Tuple
from db_connection import get_connection
from uuid import uuid4

STATUS_CODE_OK = 200


def get_holidays_by_api(year: int) -> Tuple[int, dict]:
    # https://apis.digital.gob.cl/fl/feriados/2024

    url = f'https://apis.digital.gob.cl/fl/feriados/{year}/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    return response.status_code, response_json

def process_data_api(response_json: dict) -> dict:
    connection = get_connection()
    cursor = connection.cursor()

    for holiday in response_json:
        name = holiday['nombreFeriado']
        date = holiday['fecha']
        holiday_type = holiday['tipo']
        description = holiday['descripcion']
        day_week = holiday['dia_semana']

        query = f'INSERT INTO public.holidays (id, "name", "date", "type", description, day_week) VALUES({uuid4()}, {name}, {date}, {holiday_type}, {description}, {day_week});'
        cursor.execute(query)

    connection.commit()
    cursor.close()
    

if __name__ == '__main__':
    
    for year in range(2021, 2025):
        status_code, response_json = get_holidays_by_api(year)
        print(f'Year: {year}, Status Code: {status_code}')

        if status_code == STATUS_CODE_OK:
            process_data_api(response_json)
            print('Data processed successfully')
    