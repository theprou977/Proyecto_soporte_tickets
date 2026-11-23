"""Configuración de la aplicación: lee las variables del archivo .env."""
from decouple import config

BD_HOST = config("DB_HOST", default="localhost")
BD_PUERTO = config("DB_PORT", default=3306, cast=int)
BD_USUARIO = config("DB_USER", default="root")
BD_CLAVE = config("DB_PASSWORD", default="")
BD_NOMBRE = config("DB_NAME", default="soporte_tickets")

MAX_INTENTOS_LOGIN = 3
