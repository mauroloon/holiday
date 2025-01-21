import psycopg2
from psycopg2 import Error
from db_connection import get_connection

def create_tables():
    """
    Crea la tabla en la base de datos.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        with open('create_table.sql', 'r') as sql_file:
            cursor.execute(sql_file.read())
            
        connection.commit()
        print("Tabla creada exitosamente")
        
    except Exception as error:
        print(f"Error al crear las tablas: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Conexión a PostgreSQL cerrada")

if __name__ == "__main__":
    create_tables()
