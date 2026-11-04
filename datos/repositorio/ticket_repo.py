from datos.auxiliar import fechas
from datos.modelos.enums import EstadoTicket, Prioridad
from datos.modelos.ticket import Ticket
from datos.repositorio.base import RepositorioBase


class TicketRepositorio(RepositorioBase):
    @staticmethod
    def _modelo(f):
        return Ticket(f["descripcion"], f["usuario_id"], Prioridad(f["prioridad"]),
                      EstadoTicket(f["estado"]), fechas.desde_texto(f["fecha_creacion"]),
                      f["tecnico_id"], f["id"])

    def crear(self, t):
        r = self._escribir(
            "INSERT INTO tickets (descripcion, fecha_creacion, estado, prioridad, usuario_id, tecnico_id) "
            "VALUES (:d, :f, :e, :p, :u, :t)",
            {"d": t.descripcion, "f": fechas.a_texto(t.fecha_creacion), "e": t.estado.value,
             "p": t.prioridad.value, "u": t.usuario_id, "t": t.tecnico_id})
        t.id = r.lastrowid
        return t

    def obtener(self, id):
        f = self._leer("SELECT * FROM tickets WHERE id = :i", {"i": id})
        return self._modelo(f[0]) if f else None

    def listar(self):
        return [self._modelo(f) for f in self._leer("SELECT * FROM tickets ORDER BY id")]

    def listar_por_usuario(self, usuario_id):
        return [self._modelo(f) for f in self._leer(
            "SELECT * FROM tickets WHERE usuario_id = :u ORDER BY id", {"u": usuario_id})]

    def listar_por_tecnico(self, tecnico_id):
        return [self._modelo(f) for f in self._leer(
            "SELECT * FROM tickets WHERE tecnico_id = :t ORDER BY id", {"t": tecnico_id})]

    def actualizar(self, t):
        self._escribir(
            "UPDATE tickets SET descripcion=:d, estado=:e, prioridad=:p, tecnico_id=:t WHERE id=:i",
            {"d": t.descripcion, "e": t.estado.value, "p": t.prioridad.value,
             "t": t.tecnico_id, "i": t.id})
        return t

    def eliminar(self, id):
        self._escribir("DELETE FROM tickets WHERE id = :i", {"i": id})
