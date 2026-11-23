from datos.modelos.accion_soporte import AccionSoporte
from datos.repositorios.repo_base import RepositorioBase


class AccionRepositorio(RepositorioBase):
    def crear(self, accion):
        accion.save(force_insert=True)
        return accion

    def obtener(self, id):
        return AccionSoporte.get_or_none(AccionSoporte.id == id)

    def listar(self):
        return list(AccionSoporte.select().order_by(AccionSoporte.id))

    def listar_por_ticket(self, ticket_id):
        return list(AccionSoporte.select()
                    .where(AccionSoporte.ticket == ticket_id)
                    .order_by(AccionSoporte.fecha, AccionSoporte.id))

    def actualizar(self, accion):
        accion.save()
        return accion

    def eliminar(self, id):
        AccionSoporte.delete_by_id(id)

    def listar_por_tecnico(self, tecnico_id):
        return list(AccionSoporte.select()
                    .where(AccionSoporte.tecnico == tecnico_id)
                    .order_by(AccionSoporte.id))
