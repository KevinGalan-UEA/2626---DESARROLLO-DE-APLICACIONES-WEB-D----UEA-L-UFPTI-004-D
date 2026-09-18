from flask_login import UserMixin
from conexion.conexion import obtener_conexion


class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

    @staticmethod
    def obtener_por_id(user_id):
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, usuario FROM usuarios WHERE id = %s', (user_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if fila:
            return Usuario(id=fila['id'], usuario=fila['usuario'])
        return None

    @staticmethod
    def obtener_por_usuario(nombre_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, usuario, password FROM usuarios WHERE usuario = %s', (nombre_usuario,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return fila