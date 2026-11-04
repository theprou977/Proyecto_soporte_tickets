from datos.modelos.usuario import Usuario
from datos.repositorio.base import RepositorioBase


class UsuarioRepositorio(RepositorioBase):
    @staticmethod
    def _modelo(f):
        return Usuario(f["nombre"], f["correo"], f["id"])

    def crear(self, u):
        r = self._escribir("INSERT INTO usuarios (nombre, correo) VALUES (:n, :c)",
                           {"n": u.nombre, "c": u.correo})
        u.id = r.lastrowid
        return u

    def obtener(self, id):
        f = self._leer("SELECT * FROM usuarios WHERE id = :i", {"i": id})
        return self._modelo(f[0]) if f else None

    def listar(self):
        return [self._modelo(f) for f in self._leer("SELECT * FROM usuarios ORDER BY id")]

    def existe_correo(self, correo, excluir_id=None):
        f = self._leer("SELECT id FROM usuarios WHERE correo = :c AND id <> :i",
                       {"c": correo, "i": excluir_id or -1})
        return bool(f)

    def actualizar(self, u):
        self._escribir("UPDATE usuarios SET nombre=:n, correo=:c WHERE id=:i",
                       {"n": u.nombre, "c": u.correo, "i": u.id})
        return u

    def eliminar(self, id):
        self._escribir("DELETE FROM usuarios WHERE id = :i", {"i": id})
