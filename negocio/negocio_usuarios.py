from auxiliares import mensajes, seguridad
from auxiliares.validaciones import contrasena_valida, correo_valido, texto_requerido
from datos.modelos.usuario import Usuario
from negocio.excepciones import CredencialesInvalidas, NegocioError


class ServicioUsuarios:
    def __init__(self, repo_usuarios, repo_tickets):
        self._repo = repo_usuarios
        self._tickets = repo_tickets

    # ---- autenticación ----
    def hay_usuarios(self):
        return self._repo.contar() > 0

    def autenticar(self, correo, contrasena):
        """Devuelve el Usuario si las credenciales son correctas."""
        correo = (correo or "").strip().lower()
        usuario = self._repo.obtener_por_correo(correo)
        if usuario is None:
            seguridad.verificacion_falsa(contrasena)
            raise CredencialesInvalidas(mensajes.CREDENCIALES_INVALIDAS)
        if not seguridad.verificar(contrasena, usuario.contrasena):
            raise CredencialesInvalidas(mensajes.CREDENCIALES_INVALIDAS)
        return usuario

    def cambiar_contrasena(self, id, actual, nueva):
        usuario = self.obtener(id)
        if not seguridad.verificar(actual, usuario.contrasena):
            raise NegocioError("La contraseña actual no es correcta.")
        usuario.contrasena = seguridad.hashear(contrasena_valida(nueva))
        return self._repo.actualizar(usuario)

    # ---- CRUD ----
    def crear(self, nombre, correo, contrasena):
        nombre = texto_requerido(nombre, "El nombre", 2, 80)
        correo = correo_valido(correo)
        contrasena_valida(contrasena)
        if self._repo.existe_correo(correo):
            raise NegocioError("Ya existe un usuario con ese correo.")
        usuario = Usuario(nombre=nombre, correo=correo,
                          contrasena=seguridad.hashear(contrasena))
        return self._repo.crear(usuario)

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        usuario = self._repo.obtener(id)
        if usuario is None:
            raise NegocioError(f"No existe el usuario #{id}.")
        return usuario

    def actualizar(self, id, nombre, correo):
        usuario = self.obtener(id)
        usuario.nombre = texto_requerido(nombre, "El nombre", 2, 80)
        usuario.correo = correo_valido(correo)
        if self._repo.existe_correo(usuario.correo, id):
            raise NegocioError("Ese correo ya pertenece a otro usuario.")
        return self._repo.actualizar(usuario)

    def eliminar(self, id, id_sesion=None):
        self.obtener(id)
        if id == id_sesion:
            raise NegocioError("No puedes eliminar tu propia cuenta mientras tienes la sesión abierta.")
        if self._tickets.listar_por_usuario(id):
            raise NegocioError("No se puede eliminar: el usuario tiene tickets.")
        self._repo.eliminar(id)
