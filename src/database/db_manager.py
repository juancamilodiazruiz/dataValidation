import mysql.connector
from src.config import DATABASE_CONFIG

def save_to_database(data):
    """
    Guarda los datos del DNI en la base de datos.
    :param data: Diccionario con los datos del DNI.
    """
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        query = "INSERT INTO dni_data (dni, name) VALUES (%s, %s)"
        cursor.execute(query, (data['dni'], data['name']))
        connection.commit()
        print("Datos insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error en la base de datos: {err}")
    finally:
        cursor.close()
        connection.close()
