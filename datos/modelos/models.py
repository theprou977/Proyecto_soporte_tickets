from peewee import Model

from datos.conexion_db import bd


class ModelBase(Model):
    """Clase base de Peewee: todos los modelos del proyecto heredan de ella
    para usar la misma conexión."""

    class Meta:
        database = bd
