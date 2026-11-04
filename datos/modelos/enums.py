from enum import Enum


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
