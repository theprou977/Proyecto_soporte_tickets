from auxiliares import mensajes
from auxiliares import opciones_menu as om
from presentacion import consola as c
from presentacion.presentacion_accion import PresentacionAccion
from presentacion.presentacion_tecnico import PresentacionTecnico
from presentacion.presentacion_ticket import PresentacionTicket
from presentacion.presentacion_usuario import PresentacionUsuario


class Menu:
    """Menú principal. Solo se crea después de un login exitoso."""

    def __init__(self, s_usuarios, s_tecnicos, s_tickets, s_acciones, sesion):
        self.sesion = sesion
        self._modulos = [PresentacionUsuario(s_usuarios, sesion).menu,
                         PresentacionTecnico(s_tecnicos).menu,
                         PresentacionTicket(s_tickets).menu,
                         PresentacionAccion(s_acciones).menu]

    def ejecutar(self):
        while True:
            print(f"\n===== MENÚ PRINCIPAL | sesión: {self.sesion.nombre} =====")
            for i, texto in enumerate(om.MENU_PRINCIPAL, 1):
                print(f"{i}) {texto}")
            print(f"0) {om.SALIR_SESION}")
            n = c.leer_entero("Opción: ")
            if n == 0:
                print("  Sesión cerrada.")
                return
            if 1 <= n <= len(self._modulos):
                self._modulos[n - 1]()
            else:
                print(f"  ⚠ {mensajes.OPCION_INVALIDA}")
