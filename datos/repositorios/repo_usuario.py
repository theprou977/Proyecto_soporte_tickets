from datos.modelos.usuario import Usuario
from datos.repositorios.repo_base import RepositorioBase


class UsuarioRepositorio(RepositorioBase):
    def crear(self, usuario):
        usuario.save(force_insert=True)
        return usuario

    def obtener(self, id):
        return Usuario.get_or_none(Usuario.id == id)

    def obtener_por_correo(self, correo):
        return Usuario.get_or_none(Usuario.correo == correo)

    def listar(self):
        return list(Usuario.select().order_by(Usuario.id))

    def contar(self):
        return Usuario.select().count()

    def existe_correo(self, correo, excluir_id=None):
        consulta = Usuario.select().where(Usuario.correo == correo)
        if excluir_id is not None:
            consulta = consulta.where(Usuario.id != excluir_id)
        return consulta.exists()

    def actualizar(self, usuario):
        usuario.save()
        return usuario

    def eliminar(self, id):
        Usuario.delete_by_id(id)
