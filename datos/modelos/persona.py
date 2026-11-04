from abc import ABC, abstractmethod

from datos.auxiliar.validaciones import texto_requerido


class Persona(ABC):
    """Clase base abstracta de Usuario y Tecnico (abstracción + herencia)."""

    def __init__(self, nombre, id=None):
        self._id = id
        self.nombre = nombre  # pasa por el setter (validación)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_requerido(valor, "El nombre", 2, 80)

    @abstractmethod
    def rol(self):
        """Cada subclase define su rol (polimorfismo)."""

    def describir(self):
        return f"[{self.rol()}] #{self._id} {self._nombre}"
