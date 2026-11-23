from auxiliares import fechas
from auxiliares import opciones_menu as om
from datos.modelos.enums import EstadoTicket, Prioridad
from presentacion import consola as c


class PresentacionTicket:
    def __init__(self, servicio):
        self.s = servicio

    @staticmethod
    def _fila(t):
        tecnico = f"{t.tecnico_id} - {t.tecnico.nombre}" if t.tecnico_id else "sin asignar"
        return (t.id, t.estado.value, t.prioridad.value, fechas.a_texto(t.fecha_creacion),
                f"{t.usuario_id} - {t.usuario.nombre}", tecnico, t.descripcion)

    def crear(self):
        uid = c.leer_entero("ID usuario: ")
        desc = c.leer("Descripción: ")
        prio = c.elegir_enum(Prioridad, "Prioridad:")
        print("  ✔", self.s.crear(uid, desc, prio).describir())

    def listar(self):
        c.mostrar_tabla(["ID", "Estado", "Prioridad", "Creado", "Usuario", "Técnico", "Descripción"],
                        [self._fila(t) for t in self.s.listar()])

    def detalle(self):
        tid = c.leer_entero("ID ticket: ")
        print("  " + self.s.obtener(tid).describir())
        print("  -- Historial de acciones --")
        acciones = self.s.historial(tid)
        c.mostrar_tabla(["ID", "Fecha", "Tipo", "Técnico", "Descripción"],
                        [(a.id, fechas.a_texto(a.fecha), a.tipo.value, a.tecnico_id, a.descripcion)
                         for a in acciones])

    def actualizar(self):
        tid = c.leer_entero("ID ticket: ")
        desc = c.leer("Nueva descripción: ")
        prio = c.elegir_enum(Prioridad, "Nueva prioridad:")
        print("  ✔", self.s.actualizar(tid, desc, prio).describir())

    def asignar(self):
        t = self.s.asignar(c.leer_entero("ID ticket: "), c.leer_entero("ID técnico: "))
        print("  ✔", t.describir())

    def atender(self):
        t = self.s.atender(c.leer_entero("ID ticket: "), c.leer_entero("ID técnico: "))
        print("  ✔", t.describir())

    def cambiar_estado(self):
        tid = c.leer_entero("ID ticket: ")
        nuevo = c.elegir_enum(EstadoTicket, "Nuevo estado:")
        print("  ✔", self.s.cambiar_estado(tid, nuevo).describir())

    def eliminar(self):
        id_ = c.leer_entero("ID: ")
        if c.confirmar(f"¿Eliminar el ticket #{id_} y su historial?"):
            self.s.eliminar(id_)
            print("  ✔ Eliminado")

    def menu(self):
        c.ejecutar_submenu("TICKETS", om.MENU_TICKETS,
                           [self.crear, self.listar, self.detalle, self.actualizar,
                            self.asignar, self.atender, self.cambiar_estado, self.eliminar])
