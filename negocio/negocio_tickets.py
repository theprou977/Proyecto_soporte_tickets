from auxiliares.validaciones import texto_requerido
from negocio.excepciones import NegocioError


class ServicioTickets:
    def __init__(self, repo_tickets, repo_usuarios, servicio_tecnicos, repo_acciones):
        self._repo = repo_tickets
        self._usuarios = repo_usuarios
        self._tecnicos = servicio_tecnicos
        self._acciones = repo_acciones

    def crear(self, usuario_id, descripcion, prioridad):
        usuario = self._usuarios.obtener(usuario_id)
        if usuario is None:
            raise NegocioError(f"No existe el usuario #{usuario_id}.")
        descripcion = texto_requerido(descripcion, "La descripción", 5, 300)
        return self._repo.crear(usuario.generar_ticket(descripcion, prioridad))

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        ticket = self._repo.obtener(id)
        if ticket is None:
            raise NegocioError(f"No existe el ticket #{id}.")
        return ticket

    def historial(self, id):
        self.obtener(id)
        return self._acciones.listar_por_ticket(id)

    def actualizar(self, id, descripcion, prioridad):
        ticket = self.obtener(id)
        ticket.descripcion = texto_requerido(descripcion, "La descripción", 5, 300)
        ticket.prioridad = prioridad
        return self._repo.actualizar(ticket)

    def asignar(self, ticket_id, tecnico_id):
        ticket = self.obtener(ticket_id)
        tecnico = self._tecnicos.obtener(tecnico_id)
        ticket.asignar_tecnico(tecnico)
        return self._repo.actualizar(ticket)

    def atender(self, ticket_id, tecnico_id):
        ticket = self.obtener(ticket_id)
        tecnico = self._tecnicos.obtener(tecnico_id)
        tecnico.atender_ticket(ticket)
        return self._repo.actualizar(ticket)

    def cambiar_estado(self, id, nuevo):
        ticket = self.obtener(id)
        ticket.cambiar_estado(nuevo)
        return self._repo.actualizar(ticket)

    def eliminar(self, id):
        self.obtener(id)
        self._repo.eliminar(id)  # sus acciones se borran en cascada
