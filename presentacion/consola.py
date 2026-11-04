"""Funciones de entrada/salida por consola (sin lógica de negocio)."""


def leer(mensaje):
    return input(mensaje).strip()


def leer_entero(mensaje):
    while True:
        try:
            return int(leer(mensaje))
        except ValueError:
            print("  ⚠ Ingresa un número entero.")


def elegir_enum(enum_cls, titulo):
    opciones = list(enum_cls)
    print(titulo)
    for i, o in enumerate(opciones, 1):
        print(f"  {i}) {o.value}")
    while True:
        n = leer_entero("  Opción: ")
        if 1 <= n <= len(opciones):
            return opciones[n - 1]
        print("  ⚠ Opción fuera de rango.")


def mostrar(items, vacio="  (sin registros)"):
    if not items:
        print(vacio)
    for i in items:
        print("  " + i.describir())


def pausa():
    input("\nEnter para continuar...")
