import psycopg2
from psycopg2 import Error

def get_connection():
    """
    Crea una conexión a la base de datos PostgreSQL.
    
    Returns:
        - connection: Conexión a la base de datos PostgreSQL
    """
    try:
        # NOTE: Los campos deberían ir en .env, pero en este caso de test se sube directo
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="admin123",
            host="localhost",
            port="5432"
        )
        return connection
    except Error as error:
        print(f"Error mientras se conectaba a PostgreSQL: {error}")
        raise error
