from datos.modelos.ticket import Ticket
from datos.repositorios.repo_base import RepositorioBase


class TicketRepositorio(RepositorioBase):
    def crear(self, ticket):
        ticket.save(force_insert=True)
        return ticket

    def obtener(self, id):
        return Ticket.get_or_none(Ticket.id == id)

    def listar(self):
        return list(Ticket.select().order_by(Ticket.id))

    def listar_por_usuario(self, usuario_id):
        return list(Ticket.select().where(Ticket.usuario == usuario_id).order_by(Ticket.id))

    def listar_por_tecnico(self, tecnico_id):
        return list(Ticket.select().where(Ticket.tecnico == tecnico_id).order_by(Ticket.id))

    def actualizar(self, ticket):
        ticket.save()
        return ticket

    def eliminar(self, id):
        Ticket.delete_by_id(id)  # sus acciones se borran en cascada (ON DELETE CASCADE)
