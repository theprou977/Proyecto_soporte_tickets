from datos.auxiliar.validaciones import texto_requerido
from datos.modelos.accion_soporte import AccionSoporte
from datos.modelos.enums import EstadoTicket, TipoAccion
from datos.modelos.persona import Persona


class Tecnico(Persona):
    def __init__(self, nombre, especialidad, id=None):
        super().__init__(nombre, id)
        self.especialidad = especialidad
        self._tickets = []  # tickets asignados (los carga la capa de negocio)

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self._especialidad = texto_requerido(valor, "La especialidad", 2, 80)

    @property
    def tickets(self):
        return list(self._tickets)

    @tickets.setter
    def tickets(self, lista):
        self._tickets = list(lista)

    def rol(self):
        return "Técnico"

    def describir(self):
        return f"{super().describir()} ({self._especialidad})"

    def atender_ticket(self, ticket):
        """Toma el ticket: lo asigna si hace falta y lo deja En Proceso."""
        if ticket.tecnico_id != self.id:
            ticket.asignar_tecnico(self)
        if ticket.estado == EstadoTicket.ASIGNADO:
            ticket.cambiar_estado(EstadoTicket.EN_PROCESO)
        return ticket

    def registrar_accion(self, ticket, descripcion, tipo=TipoAccion.OTRO):
        if ticket.tecnico_id != self.id:
            raise ValueError("Solo el técnico asignado puede registrar acciones.")
        return AccionSoporte(descripcion, ticket.id, self.id, tipo)

    def carga_trabajo(self):
        activos = (EstadoTicket.ASIGNADO, EstadoTicket.EN_PROCESO)
        return sum(1 for t in self._tickets if t.estado in activos)
