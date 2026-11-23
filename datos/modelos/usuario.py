from peewee import CharField

from datos.modelos.enums import Prioridad
from datos.modelos.persona import Persona


class Usuario(Persona):
    correo = CharField(max_length=120, unique=True)
    contrasena = CharField(max_length=60, null=True)  # hash Bcrypt, nunca texto plano

    class Meta:
        table_name = "usuarios"

    def rol(self):
        return "Usuario"

    def describir(self):
        return f"{super().describir()} <{self.correo}>"

    def generar_ticket(self, descripcion, prioridad=Prioridad.MEDIA):
        from datos.modelos.ticket import Ticket  # import local: evita ciclo
        if self.id is None:
            raise ValueError("El usuario debe estar guardado para generar tickets.")
        return Ticket(descripcion=descripcion, usuario=self, prioridad=prioridad)
