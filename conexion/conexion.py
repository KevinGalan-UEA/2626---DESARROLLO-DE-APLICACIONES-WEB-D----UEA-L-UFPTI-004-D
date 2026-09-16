import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'hibrido_ganador_db'
}


def obtener_conexion():
    return mysql.connector.connect(**DB_CONFIG)