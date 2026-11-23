"""Conexión a MySQL con Peewee y ejecución de los scripts SQL."""
from pathlib import Path

import pymysql
from peewee import MySQLDatabase, PeeweeException

from auxiliares.configuracion import (BD_CLAVE, BD_HOST, BD_NOMBRE, BD_PUERTO,
                                      BD_USUARIO)

# Objeto de base de datos compartido por todos los modelos (ver models.py)
bd = MySQLDatabase(BD_NOMBRE, host=BD_HOST, port=BD_PUERTO, user=BD_USUARIO,
                   password=BD_CLAVE, charset="utf8mb4")

CARPETA_SQL = Path(__file__).resolve().parent / "sql"
# 1050 tabla existe, 1060 columna duplicada, 1061 índice duplicado:
# permiten volver a ejecutar los scripts sin que falle.
_ERRORES_IGNORABLES = {1050, 1060, 1061}


def _crear_bd_si_no_existe():
    con = pymysql.connect(host=BD_HOST, port=BD_PUERTO, user=BD_USUARIO,
                          password=BD_CLAVE, charset="utf8mb4")
    try:
        with con.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{BD_NOMBRE}` "
                        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    finally:
        con.close()


def _sentencias(ruta):
    lineas = [l for l in ruta.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.strip().startswith("--")]
    return [s.strip() for s in "\n".join(lineas).split(";") if s.strip()]


def inicializar_bd():
    """Crea la BD si falta y ejecuta los .sql de datos/sql en orden cronológico
    (el nombre de cada archivo empieza con su fecha y hora)."""
    _crear_bd_si_no_existe()
    bd.connect(reuse_if_open=True)
    for script in sorted(CARPETA_SQL.glob("*.sql")):
        for sentencia in _sentencias(script):
            try:
                bd.execute_sql(sentencia)
            except PeeweeException as e:
                if not (e.args and e.args[0] in _ERRORES_IGNORABLES):
                    raise


def cerrar():
    if not bd.is_closed():
        bd.close()
