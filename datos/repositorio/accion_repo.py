from datos.auxiliar import fechas
from datos.modelos.accion_soporte import AccionSoporte
from datos.modelos.enums import TipoAccion
from datos.repositorio.base import RepositorioBase


class AccionRepositorio(RepositorioBase):
    @staticmethod
    def _modelo(f):
        return AccionSoporte(f["descripcion"], f["ticket_id"], f["tecnico_id"],
                             TipoAccion(f["tipo"]), fechas.desde_texto(f["fecha"]), f["id"])

    def crear(self, a):
        r = self._escribir(
            "INSERT INTO acciones_soporte (descripcion, fecha, tipo, ticket_id, tecnico_id) "
            "VALUES (:d, :f, :t, :ti, :te)",
            {"d": a.descripcion, "f": fechas.a_texto(a.fecha), "t": a.tipo.value,
             "ti": a.ticket_id, "te": a.tecnico_id})
        a.id = r.lastrowid
        return a

    def obtener(self, id):
        f = self._leer("SELECT * FROM acciones_soporte WHERE id = :i", {"i": id})
        return self._modelo(f[0]) if f else None

    def listar(self):
        return [self._modelo(f) for f in self._leer("SELECT * FROM acciones_soporte ORDER BY id")]

    def listar_por_ticket(self, ticket_id):
        return [self._modelo(f) for f in self._leer(
            "SELECT * FROM acciones_soporte WHERE ticket_id = :t ORDER BY fecha, id", {"t": ticket_id})]

    def actualizar(self, a):
        self._escribir("UPDATE acciones_soporte SET descripcion=:d, tipo=:t WHERE id=:i",
                       {"d": a.descripcion, "t": a.tipo.value, "i": a.id})
        return a

    def eliminar(self, id):
        self._escribir("DELETE FROM acciones_soporte WHERE id = :i", {"i": id})
