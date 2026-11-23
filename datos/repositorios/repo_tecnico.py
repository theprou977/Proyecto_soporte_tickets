from datos.modelos.tecnico import Tecnico
from datos.repositorios.repo_base import RepositorioBase


class TecnicoRepositorio(RepositorioBase):
    def crear(self, tecnico):
        tecnico.save(force_insert=True)
        return tecnico

    def obtener(self, id):
        return Tecnico.get_or_none(Tecnico.id == id)

    def listar(self):
        return list(Tecnico.select().order_by(Tecnico.id))

    def actualizar(self, tecnico):
        tecnico.save()
        return tecnico

    def eliminar(self, id):
        Tecnico.delete_by_id(id)
