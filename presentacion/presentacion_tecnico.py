from auxiliares import opciones_menu as om
from presentacion import consola as c


class PresentacionTecnico:
    def __init__(self, servicio):
        self.s = servicio

    def crear(self):
        print("  ✔", self.s.crear(c.leer("Nombre: "), c.leer("Especialidad: ")).describir())

    def listar(self):
        c.mostrar_tabla(["ID", "Nombre", "Especialidad", "Carga"],
                        [(t.id, t.nombre, t.especialidad, t.carga_trabajo())
                         for t in self.s.listar()])

    def actualizar(self):
        tecnico = self.s.actualizar(c.leer_entero("ID: "), c.leer("Nuevo nombre: "),
                                    c.leer("Nueva especialidad: "))
        print("  ✔", tecnico.describir())

    def eliminar(self):
        id_ = c.leer_entero("ID: ")
        if c.confirmar(f"¿Eliminar el técnico #{id_}?"):
            self.s.eliminar(id_)
            print("  ✔ Eliminado")

    def carga(self):
        t = self.s.obtener(c.leer_entero("ID técnico: "))
        print(f"  {t.describir()} → carga de trabajo: {t.carga_trabajo()}")

    def menu(self):
        c.ejecutar_submenu("TÉCNICOS", om.MENU_TECNICOS,
                           [self.crear, self.listar, self.actualizar, self.eliminar, self.carga])
