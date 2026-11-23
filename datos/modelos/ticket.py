from peewee import CharField, DateTimeField, ForeignKeyField

from auxiliares import fechas
from datos.modelos.enums import CampoEnum, EstadoTicket, Prioridad
from datos.modelos.models import ModelBase
from datos.modelos.tecnico import Tecnico
from datos.modelos.usuario import Usuario

# Reglas de transición del ciclo de vida del ticket
TRANSICIONES = {
    EstadoTicket.ABIERTO: {EstadoTicket.ASIGNADO, EstadoTicket.CERRADO},
    EstadoTicket.ASIGNADO: {EstadoTicket.EN_PROCESO, EstadoTicket.CERRADO},
    EstadoTicket.EN_PROCESO: {EstadoTicket.RESUELTO, EstadoTicket.ASIGNADO},
    EstadoTicket.RESUELTO: {EstadoTicket.CERRADO, EstadoTicket.EN_PROCESO},
    EstadoTicket.CERRADO: set(),
}


class Ticket(ModelBase):
    descripcion = CharField(max_length=300)
    fecha_creacion = DateTimeField(default=fechas.ahora)
    estado = CampoEnum(EstadoTicket, max_length=20, default=EstadoTicket.ABIERTO)
    prioridad = CampoEnum(Prioridad, max_length=20, default=Prioridad.MEDIA)
    usuario = ForeignKeyField(Usuario, backref="tickets", column_name="usuario_id",
                              on_delete="RESTRICT")
    tecnico = ForeignKeyField(Tecnico, backref="tickets", column_name="tecnico_id",
                              null=True, on_delete="SET NULL")

    class Meta:
        table_name = "tickets"

    def cambiar_estado(self, nuevo):
        if nuevo not in TRANSICIONES[self.estado]:
            raise ValueError(
                f"No se puede pasar de {self.estado.value} a {nuevo.value}.")
        if nuevo in (EstadoTicket.EN_PROCESO, EstadoTicket.RESUELTO) and self.tecnico_id is None:
            raise ValueError("El ticket necesita un técnico asignado.")
        self.estado = nuevo
        return self.estado

    def asignar_tecnico(self, tecnico):
        if self.estado not in (EstadoTicket.ABIERTO, EstadoTicket.ASIGNADO):
            raise ValueError("Solo se puede asignar técnico a tickets Abiertos o Asignados.")
        if tecnico.id is None:
            raise ValueError("El técnico debe estar guardado.")
        self.tecnico = tecnico
        self.estado = EstadoTicket.ASIGNADO
        return tecnico

    def describir(self):
        tec = self.tecnico_id if self.tecnico_id else "sin asignar"
        return (f"Ticket #{self.id} | {self.estado.value} | {self.prioridad.value} | "
                f"{fechas.a_texto(self.fecha_creacion)} | usuario {self.usuario_id} | "
                f"técnico {tec}\n    {self.descripcion}")
