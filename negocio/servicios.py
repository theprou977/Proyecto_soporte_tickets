from datos.modelos.tecnico import Tecnico
from datos.modelos.usuario import Usuario
from negocio.excepciones import NegocioError


class ServicioUsuarios:
    def __init__(self, repo_usuarios, repo_tickets):
        self._repo = repo_usuarios
        self._tickets = repo_tickets

    def crear(self, nombre, correo):
        u = Usuario(nombre, correo)
        if self._repo.existe_correo(u.correo):
            raise NegocioError("Ya existe un usuario con ese correo.")
        return self._repo.crear(u)

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        u = self._repo.obtener(id)
        if u is None:
            raise NegocioError(f"No existe el usuario #{id}.")
        return u

    def actualizar(self, id, nombre, correo):
        u = self.obtener(id)
        u.nombre, u.correo = nombre, correo
        if self._repo.existe_correo(u.correo, id):
            raise NegocioError("Ese correo ya pertenece a otro usuario.")
        return self._repo.actualizar(u)

    def eliminar(self, id):
        self.obtener(id)
        if self._tickets.listar_por_usuario(id):
            raise NegocioError("No se puede eliminar: el usuario tiene tickets.")
        self._repo.eliminar(id)


class ServicioTecnicos:
    def __init__(self, repo_tecnicos, repo_tickets):
        self._repo = repo_tecnicos
        self._tickets = repo_tickets

    def crear(self, nombre, especialidad):
        return self._repo.crear(Tecnico(nombre, especialidad))

    def _cargar(self, t):
        t.tickets = self._tickets.listar_por_tecnico(t.id)
        return t

    def listar(self):
        return [self._cargar(t) for t in self._repo.listar()]

    def obtener(self, id):
        t = self._repo.obtener(id)
        if t is None:
            raise NegocioError(f"No existe el técnico #{id}.")
        return self._cargar(t)

    def actualizar(self, id, nombre, especialidad):
        t = self.obtener(id)
        t.nombre, t.especialidad = nombre, especialidad
        return self._repo.actualizar(t)

    def eliminar(self, id):
        t = self.obtener(id)
        if t.carga_trabajo() > 0:
            raise NegocioError("No se puede eliminar: tiene tickets en curso.")
        self._repo.eliminar(id)


class ServicioTickets:
    def __init__(self, repo_tickets, repo_usuarios, servicio_tecnicos, repo_acciones):
        self._repo = repo_tickets
        self._usuarios = repo_usuarios
        self._tecnicos = servicio_tecnicos
        self._acciones = repo_acciones

    def crear(self, usuario_id, descripcion, prioridad):
        usuario = self._usuarios.obtener(usuario_id)
        if usuario is None:
            raise NegocioError(f"No existe el usuario #{usuario_id}.")
        return self._repo.crear(usuario.generar_ticket(descripcion, prioridad))

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        t = self._repo.obtener(id)
        if t is None:
            raise NegocioError(f"No existe el ticket #{id}.")
        return t

    def historial(self, id):
        self.obtener(id)
        return self._acciones.listar_por_ticket(id)

    def actualizar(self, id, descripcion, prioridad):
        t = self.obtener(id)
        t.descripcion, t.prioridad = descripcion, prioridad
        return self._repo.actualizar(t)

    def asignar(self, ticket_id, tecnico_id):
        t = self.obtener(ticket_id)
        tec = self._tecnicos.obtener(tecnico_id)
        t.asignar_tecnico(tec)
        return self._repo.actualizar(t)

    def atender(self, ticket_id, tecnico_id):
        t = self.obtener(ticket_id)
        tec = self._tecnicos.obtener(tecnico_id)
        tec.atender_ticket(t)
        return self._repo.actualizar(t)

    def cambiar_estado(self, id, nuevo):
        t = self.obtener(id)
        t.cambiar_estado(nuevo)
        return self._repo.actualizar(t)

    def eliminar(self, id):
        self.obtener(id)
        self._repo.eliminar(id)  # sus acciones se borran en cascada


class ServicioAcciones:
    def __init__(self, repo_acciones, servicio_tickets, servicio_tecnicos):
        self._repo = repo_acciones
        self._tickets = servicio_tickets
        self._tecnicos = servicio_tecnicos

    def registrar(self, tecnico_id, ticket_id, descripcion, tipo):
        tec = self._tecnicos.obtener(tecnico_id)
        ticket = self._tickets.obtener(ticket_id)
        return self._repo.crear(tec.registrar_accion(ticket, descripcion, tipo))

    def listar(self):
        return self._repo.listar()

    def obtener(self, id):
        a = self._repo.obtener(id)
        if a is None:
            raise NegocioError(f"No existe la acción #{id}.")
        return a

    def actualizar(self, id, descripcion, tipo):
        a = self.obtener(id)
        a.descripcion, a.tipo = descripcion, tipo
        return self._repo.actualizar(a)

    def eliminar(self, id):
        self.obtener(id)
        self._repo.eliminar(id)
