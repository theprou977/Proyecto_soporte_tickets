from datos.modelos.tecnico import Tecnico
from datos.repositorio.base import RepositorioBase


class TecnicoRepositorio(RepositorioBase):
    @staticmethod
    def _modelo(f):
        return Tecnico(f["nombre"], f["especialidad"], f["id"])

    def crear(self, t):
        r = self._escribir("INSERT INTO tecnicos (nombre, especialidad) VALUES (:n, :e)",
                           {"n": t.nombre, "e": t.especialidad})
        t.id = r.lastrowid
        return t

    def obtener(self, id):
        f = self._leer("SELECT * FROM tecnicos WHERE id = :i", {"i": id})
        return self._modelo(f[0]) if f else None

    def listar(self):
        return [self._modelo(f) for f in self._leer("SELECT * FROM tecnicos ORDER BY id")]

    def actualizar(self, t):
        self._escribir("UPDATE tecnicos SET nombre=:n, especialidad=:e WHERE id=:i",
                       {"n": t.nombre, "e": t.especialidad, "i": t.id})
        return t

    def eliminar(self, id):
        self._escribir("DELETE FROM tecnicos WHERE id = :i", {"i": id})
