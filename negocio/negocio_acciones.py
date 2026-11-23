from auxiliares.validaciones import texto_requerido
from negocio.excepciones import NegocioError


class ServicioAcciones:
    def __init__(self, repo_acciones, servicio_tickets, servicio_tecnicos):
        self._repo = repo_acciones
        self._tickets = servicio_tickets
        self._tecnicos = servicio_tecnicos

    def registrar(self, tecnico_id, ticket_id, descripcion, tipo):
        tecnico = self._tecnicos.obtener(tecnico_id)
        ticket = self._tickets.obtener(ticket_id)
        descripcion = texto_requerido(descripcion, "La descripción", 3, 300)
        return self._repo.crear(tecnico.registrar_accion(ticket, descripcion, tipo))

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        accion = self._repo.obtener(id)
        if accion is None:
            raise NegocioError(f"No existe la acción #{id}.")
        return accion

    def actualizar(self, id, descripcion, tipo):
        accion = self.obtener(id)
        accion.descripcion = texto_requerido(descripcion, "La descripción", 3, 300)
        accion.tipo = tipo
        return self._repo.actualizar(accion)

    def eliminar(self, id):
        self.obtener(id)
        self._repo.eliminar(id)
