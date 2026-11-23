from auxiliares.validaciones import texto_requerido
from datos.modelos.tecnico import Tecnico
from negocio.excepciones import NegocioError


class ServicioTecnicos:
    def __init__(self, repo_tecnicos, repo_acciones):
        self._repo = repo_tecnicos
        self._acciones = repo_acciones

    def crear(self, nombre, especialidad):
        tecnico = Tecnico(nombre=texto_requerido(nombre, "El nombre", 2, 80),
                          especialidad=texto_requerido(especialidad, "La especialidad", 2, 80))
        return self._repo.crear(tecnico)

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        tecnico = self._repo.obtener(id)
        if tecnico is None:
            raise NegocioError(f"No existe el técnico #{id}.")
        return tecnico

    def actualizar(self, id, nombre, especialidad):
        tecnico = self.obtener(id)
        tecnico.nombre = texto_requerido(nombre, "El nombre", 2, 80)
        tecnico.especialidad = texto_requerido(especialidad, "La especialidad", 2, 80)
        return self._repo.actualizar(tecnico)

    def eliminar(self, id):
        tecnico = self.obtener(id)
        if tecnico.carga_trabajo() > 0:
            raise NegocioError("No se puede eliminar: tiene tickets en curso.")
        if self._acciones.listar_por_tecnico(id):
            raise NegocioError("No se puede eliminar: tiene acciones de soporte registradas.")
        self._repo.eliminar(id)
