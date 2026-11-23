"""Punto de entrada: python main.py  (inicia siempre con el login)."""
from peewee import OperationalError

from auxiliares import info_app, mensajes
from datos.conexion import cerrar, inicializar_bd
from datos.repositorios.repo_accion import AccionRepositorio
from datos.repositorios.repo_tecnico import TecnicoRepositorio
from datos.repositorios.repo_ticket import TicketRepositorio
from datos.repositorios.repo_usuario import UsuarioRepositorio
from negocio.negocio_acciones import ServicioAcciones
from negocio.negocio_tecnicos import ServicioTecnicos
from negocio.negocio_tickets import ServicioTickets
from negocio.negocio_usuarios import ServicioUsuarios
from presentacion.menu import Menu
from presentacion.presentacion_login import PresentacionLogin


def main():
    print(info_app.banner())
    try:
        inicializar_bd()

        r_usuarios, r_tecnicos = UsuarioRepositorio(), TecnicoRepositorio()
        r_tickets, r_acciones = TicketRepositorio(), AccionRepositorio()

        s_usuarios = ServicioUsuarios(r_usuarios, r_tickets)
        s_tecnicos = ServicioTecnicos(r_tecnicos, r_acciones)
        s_tickets = ServicioTickets(r_tickets, r_usuarios, s_tecnicos, r_acciones)
        s_acciones = ServicioAcciones(r_acciones, s_tickets, s_tecnicos)

        login = PresentacionLogin(s_usuarios)
        while True:
            sesion = login.iniciar_sesion()  # sin login no hay acceso al menú
            if sesion is None:
                break
            Menu(s_usuarios, s_tecnicos, s_tickets, s_acciones, sesion).ejecutar()
    except OperationalError:
        print(f"\n⚠ {mensajes.ERROR_CONEXION}")
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        cerrar()
    print(mensajes.DESPEDIDA)


if __name__ == "__main__":
    main()
