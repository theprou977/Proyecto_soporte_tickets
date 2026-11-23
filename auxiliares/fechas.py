from datetime import datetime


def ahora():
    return datetime.now().replace(microsecond=0)


def a_texto(fecha):
    return fecha.strftime("%Y-%m-%d %H:%M") if fecha else "-"
