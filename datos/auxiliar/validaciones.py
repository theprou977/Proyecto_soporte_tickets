import re

_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def texto_requerido(valor, campo, minimo=2, maximo=300):
    """Valida que un texto exista y esté dentro de un largo razonable."""
    if valor is None or not str(valor).strip():
        raise ValueError(f"{campo} es obligatorio.")
    limpio = str(valor).strip()
    if len(limpio) < minimo:
        raise ValueError(f"{campo} debe tener al menos {minimo} caracteres.")
    if len(limpio) > maximo:
        raise ValueError(f"{campo} no puede superar {maximo} caracteres.")
    return limpio


def correo_valido(valor):
    limpio = texto_requerido(valor, "El correo", 5, 120).lower()
    if not _PATRON_CORREO.match(limpio):
        raise ValueError("El correo no tiene un formato válido.")
    return limpio
