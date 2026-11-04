from datos.conexion.conexion import Conexion
from datos.repositorio.accion_repo import AccionRepositorio
from datos.repositorio.tecnico_repo import TecnicoRepositorio
from datos.repositorio.ticket_repo import TicketRepositorio
from datos.repositorio.usuario_repo import UsuarioRepositorio
from negocio.servicios import (ServicioAcciones, ServicioTecnicos,
                               ServicioTickets, ServicioUsuarios)
from presentacion.menu import Menu


def main():
    Conexion().inicializar_bd()

    r_usuarios, r_tecnicos = UsuarioRepositorio(), TecnicoRepositorio()
    r_tickets, r_acciones = TicketRepositorio(), AccionRepositorio()

    s_usuarios = ServicioUsuarios(r_usuarios, r_tickets)
    s_tecnicos = ServicioTecnicos(r_tecnicos, r_tickets)
    s_tickets = ServicioTickets(r_tickets, r_usuarios, s_tecnicos, r_acciones)
    s_acciones = ServicioAcciones(r_acciones, s_tickets, s_tecnicos)

    Menu(s_usuarios, s_tecnicos, s_tickets, s_acciones).ejecutar()


if __name__ == "__main__":
    main()
