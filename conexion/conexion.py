import os
import psycopg2


def obtener_conexion():
    """Crea y devuelve una nueva conexión a PostgreSQL.

    Si existe la variable de entorno DATABASE_URL (como en Render), se usa esa.
    Si no, se usa la configuración local (tu PostgreSQL instalado en tu computadora).
    """
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='admin357',
        dbname='hibrido_ganador_db'
    )