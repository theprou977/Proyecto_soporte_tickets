from auxiliares import opciones_menu as om
from presentacion import consola as c


class PresentacionUsuario:
    def __init__(self, servicio, sesion):
        self.s = servicio
        self.sesion = sesion  # usuario con la sesión iniciada

    def crear(self):
        usuario = self.s.crear(c.leer("Nombre: "), c.leer("Correo: "),
                               c.leer_contrasena_nueva("Contraseña: "))
        print("  ✔", usuario.describir())

    def listar(self):
        c.mostrar_tabla(["ID", "Nombre", "Correo"],
                        [(u.id, u.nombre, u.correo) for u in self.s.listar()])

    def actualizar(self):
        usuario = self.s.actualizar(c.leer_entero("ID: "), c.leer("Nuevo nombre: "),
                                    c.leer("Nuevo correo: "))
        print("  ✔", usuario.describir())

    def cambiar_contrasena(self):
        actual = c.leer_contrasena("Contraseña actual: ")
        nueva = c.leer_contrasena_nueva()
        self.s.cambiar_contrasena(self.sesion.id, actual, nueva)
        print("  ✔ Contraseña actualizada")

    def eliminar(self):
        id_ = c.leer_entero("ID: ")
        if c.confirmar(f"¿Eliminar el usuario #{id_}?"):
            self.s.eliminar(id_, self.sesion.id)
            print("  ✔ Eliminado")

    def menu(self):
        c.ejecutar_submenu("USUARIOS", om.MENU_USUARIOS,
                           [self.crear, self.listar, self.actualizar,
                            self.cambiar_contrasena, self.eliminar])
