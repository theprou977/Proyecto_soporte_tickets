from datos.auxiliar import fechas
from datos.auxiliar.validaciones import texto_requerido
from datos.modelos.enums import EstadoTicket, Prioridad

# Reglas de transición del ciclo de vida del ticket
TRANSICIONES = {
    EstadoTicket.ABIERTO: {EstadoTicket.ASIGNADO, EstadoTicket.CERRADO},
    EstadoTicket.ASIGNADO: {EstadoTicket.EN_PROCESO, EstadoTicket.CERRADO},
    EstadoTicket.EN_PROCESO: {EstadoTicket.RESUELTO, EstadoTicket.ASIGNADO},
    EstadoTicket.RESUELTO: {EstadoTicket.CERRADO, EstadoTicket.EN_PROCESO},
    EstadoTicket.CERRADO: set(),
}


class Ticket:
    def __init__(self, descripcion, usuario_id, prioridad=Prioridad.MEDIA,
                 estado=EstadoTicket.ABIERTO, fecha_creacion=None,
                 tecnico_id=None, id=None):
        self._id = id
        self.descripcion = descripcion
        self._usuario_id = usuario_id
        self.prioridad = prioridad
        self._estado = estado
        self._fecha_creacion = fecha_creacion or fechas.ahora()
        self._tecnico_id = tecnico_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = texto_requerido(valor, "La descripción", 5, 300)

    @property
    def prioridad(self):
        return self._prioridad

    @prioridad.setter
    def prioridad(self, valor):
        if not isinstance(valor, Prioridad):
            raise ValueError("Prioridad inválida.")
        self._prioridad = valor

    @property
    def estado(self):
        return self._estado

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def tecnico_id(self):
        return self._tecnico_id

    def cambiar_estado(self, nuevo):
        if nuevo not in TRANSICIONES[self._estado]:
            raise ValueError(
                f"No se puede pasar de {self._estado.value} a {nuevo.value}.")
        if nuevo in (EstadoTicket.EN_PROCESO, EstadoTicket.RESUELTO) and self._tecnico_id is None:
            raise ValueError("El ticket necesita un técnico asignado.")
        self._estado = nuevo
        return self._estado

    def asignar_tecnico(self, tecnico):
        if self._estado not in (EstadoTicket.ABIERTO, EstadoTicket.ASIGNADO):
            raise ValueError("Solo se puede asignar técnico a tickets Abiertos o Asignados.")
        if tecnico.id is None:
            raise ValueError("El técnico debe estar guardado.")
        self._tecnico_id = tecnico.id
        self._estado = EstadoTicket.ASIGNADO
        return tecnico

    def describir(self):
        tec = self._tecnico_id if self._tecnico_id else "sin asignar"
        return (f"Ticket #{self._id} | {self._estado.value} | {self._prioridad.value} | "
                f"{fechas.a_texto(self._fecha_creacion)} | usuario {self._usuario_id} | "
                f"técnico {tec}\n    {self._descripcion}")
