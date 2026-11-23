from auxiliares import fechas
from auxiliares import opciones_menu as om
from datos.modelos.enums import TipoAccion
from presentacion import consola as c


class PresentacionAccion:
    def __init__(self, servicio):
        self.s = servicio

    def registrar(self):
        tec = c.leer_entero("ID técnico: ")
        tic = c.leer_entero("ID ticket: ")
        desc = c.leer("Descripción: ")
        tipo = c.elegir_enum(TipoAccion, "Tipo de acción:")
        print("  ✔", self.s.registrar(tec, tic, desc, tipo).describir())

    def listar(self):
        c.mostrar_tabla(["ID", "Fecha", "Tipo", "Ticket", "Técnico", "Descripción"],
                        [(a.id, fechas.a_texto(a.fecha), a.tipo.value, a.ticket_id,
                          a.tecnico_id, a.descripcion) for a in self.s.listar()])

    def actualizar(self):
        aid = c.leer_entero("ID acción: ")
        desc = c.leer("Nueva descripción: ")
        tipo = c.elegir_enum(TipoAccion, "Nuevo tipo:")
        print("  ✔", self.s.actualizar(aid, desc, tipo).describir())

    def eliminar(self):
        id_ = c.leer_entero("ID: ")
        if c.confirmar(f"¿Eliminar la acción #{id_}?"):
            self.s.eliminar(id_)
            print("  ✔ Eliminada")

    def menu(self):
        c.ejecutar_submenu("ACCIONES DE SOPORTE", om.MENU_ACCIONES,
                           [self.registrar, self.listar, self.actualizar, self.eliminar])
