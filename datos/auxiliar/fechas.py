from datetime import datetime


def ahora():
    return datetime.now().replace(microsecond=0)


def a_texto(fecha):
    return fecha.isoformat(sep=" ")


def desde_texto(texto):
    return datetime.fromisoformat(texto)
