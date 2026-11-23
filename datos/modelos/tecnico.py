from peewee import CharField

from datos.modelos.enums import EstadoTicket, TipoAccion
from datos.modelos.persona import Persona


class Tecnico(Persona):
    especialidad = CharField(max_length=80)

    class Meta:
        table_name = "tecnicos"

    def rol(self):
        return "Técnico"

    def describir(self):
        return f"{super().describir()} ({self.especialidad})"

    def atender_ticket(self, ticket):
        """Toma el ticket: lo asigna si hace falta y lo deja En Proceso."""
        if ticket.tecnico_id != self.id:
            ticket.asignar_tecnico(self)
        if ticket.estado == EstadoTicket.ASIGNADO:
            ticket.cambiar_estado(EstadoTicket.EN_PROCESO)
        return ticket

    def registrar_accion(self, ticket, descripcion, tipo=TipoAccion.OTRO):
        from datos.modelos.accion_soporte import AccionSoporte  # evita ciclo
        if ticket.tecnico_id != self.id:
            raise ValueError("Solo el técnico asignado puede registrar acciones.")
        return AccionSoporte(descripcion=descripcion, ticket=ticket,
                             tecnico=self, tipo=tipo)

    def carga_trabajo(self):
        activos = [EstadoTicket.ASIGNADO, EstadoTicket.EN_PROCESO]
        consulta = self.tickets  # backref creado por Ticket.tecnico
        return consulta.where(consulta.model.estado.in_(activos)).count()
