import psycopg2
from psycopg2 import Error

def get_connection():
    try:
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
