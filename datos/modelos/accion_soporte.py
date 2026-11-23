from peewee import CharField, DateTimeField, ForeignKeyField

from auxiliares import fechas
from datos.modelos.enums import CampoEnum, TipoAccion
from datos.modelos.models import ModelBase
from datos.modelos.tecnico import Tecnico
from datos.modelos.ticket import Ticket


class AccionSoporte(ModelBase):
    descripcion = CharField(max_length=300)
    fecha = DateTimeField(default=fechas.ahora)
    tipo = CampoEnum(TipoAccion, max_length=20, default=TipoAccion.OTRO)
    ticket = ForeignKeyField(Ticket, backref="acciones", column_name="ticket_id",
                             on_delete="CASCADE")
    tecnico = ForeignKeyField(Tecnico, backref="acciones", column_name="tecnico_id")

    class Meta:
        table_name = "acciones_soporte"

    def describir(self):
        return (f"Acción #{self.id} | {self.tipo.value} | {fechas.a_texto(self.fecha)} | "
                f"ticket {self.ticket_id} | técnico {self.tecnico_id}\n    {self.descripcion}")
