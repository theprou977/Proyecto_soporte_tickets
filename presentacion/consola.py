"""Entrada/salida por consola (sin lógica de negocio)."""
import maskpass
from peewee import PeeweeException
from prettytable import PrettyTable

from auxiliares import mensajes
from negocio.excepciones import NegocioError


def leer(mensaje):
    return input(mensaje).strip()


def leer_contrasena(mensaje="Contraseña: "):
    """Pide la contraseña mostrando asteriscos (Maskpass)."""
    return maskpass.askpass(prompt=mensaje, mask="*")


def leer_contrasena_nueva(mensaje="Nueva contraseña: "):
    """Pide la contraseña dos veces para evitar errores de tipeo."""
    print(f"  ({mensajes.CONTRASENA_REQUISITOS})")
    primera = leer_contrasena(mensaje)
    segunda = leer_contrasena("Repite la contraseña: ")
    if primera != segunda:
        raise ValueError("Las contraseñas no coinciden.")
    return primera


def leer_entero(mensaje):
    while True:
        try:
            return int(leer(mensaje))
        except ValueError:
            print(f"  ⚠ {mensajes.ENTERO_REQUERIDO}")


def elegir_enum(enum_cls, titulo):
    opciones = list(enum_cls)
    print(titulo)
    for i, o in enumerate(opciones, 1):
        print(f"  {i}) {o.value}")
    while True:
        n = leer_entero("  Opción: ")
        if 1 <= n <= len(opciones):
            return opciones[n - 1]
        print(f"  ⚠ {mensajes.FUERA_DE_RANGO}")


def confirmar(pregunta):
    return leer(f"{pregunta} (s/n): ").lower() in ("s", "si", "sí")


def mostrar_tabla(columnas, filas, vacio=mensajes.SIN_REGISTROS):
    if not filas:
        print(f"  {vacio}")
        return
    tabla = PrettyTable(columnas)
    tabla.align = "l"
    for fila in filas:
        tabla.add_row(fila)
    print(tabla)


def pausa():
    input("\nEnter para continuar...")


def ejecutar_submenu(titulo, textos, acciones):
    """Muestra un submenú y repite hasta elegir 0. textos y acciones van en el mismo orden."""
    while True:
        print(f"\n=== {titulo} ===")
        for i, texto in enumerate(textos, 1):
            print(f"{i}) {texto}")
        print("0) Volver")
        n = leer_entero("Opción: ")
        if n == 0:
            return
        if not 1 <= n <= len(acciones):
            print(f"  ⚠ {mensajes.OPCION_INVALIDA}")
            continue
        try:
            acciones[n - 1]()
        except (ValueError, NegocioError) as e:
            print(f"  ⚠ {e}")
        except PeeweeException as e:
            print(f"  ⚠ {mensajes.ERROR_BD} ({e.__class__.__name__})")
        pausa()
