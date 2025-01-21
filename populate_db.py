from enum import Enum
import requests

from typing import Tuple
from db_connection import get_connection
from uuid import uuid4
from datetime import datetime

STATUS_CODE_OK = 200

class WeekDaysTranslations(Enum):
    MONDAY = 'Lunes'
    TUESDAY = 'Martes'
    WEDNESDAY = 'Miércoles'
    THURSDAY = 'Jueves'
    FRIDAY = 'Viernes'
    SATURDAY = 'Sábado'
    SUNDAY = 'Domingo'


def get_holidays_by_api(year: int) -> Tuple[int, dict]:
    """
    Obtiene los feriados de un año específico desde la API de feriados del gobierno de Chile.
    
    Args:
        - year (int): Año a consultar
        
    Returns:
        - Tuple[int, dict]: Código de estado de la respuesta y diccionario con los feriados
    """
    url = f'https://apis.digital.gob.cl/fl/feriados/{year}/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response_json = response.json()
        return response.status_code, response_json
    except requests.exceptions.Timeout:
        print(f"Timeout error fetching data for year {year}")
        return 408, {}

def process_data_api(response_json: dict) -> dict:
    """
    Procesa los datos obtenidos desde la API de feriados y los inserta en la base de datos.
    
    Args:
        - response_json (dict): Diccionario con los feriados
        
    Returns:
        - dict: Diccionario con los feriados
    """
    connection = get_connection()
    cursor = connection.cursor()

    for holiday in response_json:
        name = holiday['nombre']
        date = holiday['fecha']
        holiday_type = holiday['tipo']
        description = holiday['comentarios']
        id_holiday = uuid4().hex
        
        date_formate = datetime.strptime(date, '%Y-%m-%d').date()
        day_week = date_formate.strftime('%A')
        day_week = WeekDaysTranslations[day_week.upper()].value
        
        try:
            query = 'INSERT INTO public.holidays (id, "name", "date", "type", description, day_week) VALUES(%s, %s, %s, %s, %s, %s);'
            cursor.execute(query, (id_holiday, name, date, holiday_type, description, day_week))
        except Exception as e:
            print(f"Error inserting holiday {name}: {str(e)}")
            connection.rollback()

    connection.commit()
    cursor.close()
    

if __name__ == '__main__':
    for year in range(2021, 2025):
        status_code, response_json = get_holidays_by_api(year)
        print(f'Year: {year}, Status Code: {status_code}')

        if status_code == STATUS_CODE_OK:
            process_data_api(response_json)
            print('Data processed successfully')
        else:
            print(f'Error fetching data of year: {year}')