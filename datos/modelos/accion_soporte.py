from datos.auxiliar import fechas
from datos.auxiliar.validaciones import texto_requerido
from datos.modelos.enums import TipoAccion


class AccionSoporte:
    def __init__(self, descripcion, ticket_id, tecnico_id, tipo=TipoAccion.OTRO,
                 fecha=None, id=None):
        self._id = id
        self.descripcion = descripcion
        self.tipo = tipo
        self._fecha = fecha or fechas.ahora()
        self._ticket_id = ticket_id
        self._tecnico_id = tecnico_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = texto_requerido(valor, "La descripción", 3, 300)

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if not isinstance(valor, TipoAccion):
            raise ValueError("Tipo de acción inválido.")
        self._tipo = valor

    @property
    def fecha(self):
        return self._fecha

    @property
    def ticket_id(self):
        return self._ticket_id

    @property
    def tecnico_id(self):
        return self._tecnico_id

    def describir(self):
        return (f"Acción #{self._id} | {self._tipo.value} | {fechas.a_texto(self._fecha)} | "
                f"ticket {self._ticket_id} | técnico {self._tecnico_id}\n    {self._descripcion}")
