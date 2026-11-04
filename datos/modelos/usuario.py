from datos.auxiliar.validaciones import correo_valido
from datos.modelos.enums import Prioridad
from datos.modelos.persona import Persona
from datos.modelos.ticket import Ticket


class Usuario(Persona):
    def __init__(self, nombre, correo, id=None):
        super().__init__(nombre, id)
        self.correo = correo

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = correo_valido(valor)

    def rol(self):
        return "Usuario"

    def describir(self):
        return f"{super().describir()} <{self._correo}>"

    def generar_ticket(self, descripcion, prioridad=Prioridad.MEDIA):
        if self.id is None:
            raise ValueError("El usuario debe estar guardado para generar tickets.")
        return Ticket(descripcion, self.id, prioridad)
