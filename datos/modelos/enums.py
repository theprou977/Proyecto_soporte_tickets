from enum import Enum

from peewee import CharField


class EstadoTicket(Enum):
    ABIERTO = "Abierto"
    ASIGNADO = "Asignado"
    EN_PROCESO = "EnProceso"
    RESUELTO = "Resuelto"
    CERRADO = "Cerrado"


class Prioridad(Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Critica"


class TipoAccion(Enum):
    DIAGNOSTICO = "Diagnostico"
    REPARACION = "Reparacion"
    CONSULTA = "Consulta"
    ESCALAMIENTO = "Escalamiento"
    OTRO = "Otro"


class CampoEnum(CharField):
    """Campo de Peewee que guarda el valor de un Enum y devuelve el Enum."""

    def __init__(self, enum_cls, *args, **kwargs):
        self.enum_cls = enum_cls
        super().__init__(*args, **kwargs)

    def db_value(self, valor):
        if valor is None:
            return None
        if isinstance(valor, self.enum_cls):
            return valor.value
        return self.enum_cls(valor).value

    def python_value(self, valor):
        return None if valor is None else self.enum_cls(valor)
