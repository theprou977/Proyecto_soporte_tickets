from peewee import CharField

from datos.modelos.models import ModelBase


class Persona(ModelBase):
    """Clase base de Usuario y Tecnico (herencia). No tiene tabla propia:
    sus campos se heredan a las tablas de cada subclase."""

    nombre = CharField(max_length=80)

    def rol(self):
        """Cada subclase define su rol (polimorfismo)."""
        raise NotImplementedError("La subclase debe definir su rol.")

    def describir(self):
        return f"[{self.rol()}] #{self.id} {self.nombre}"
