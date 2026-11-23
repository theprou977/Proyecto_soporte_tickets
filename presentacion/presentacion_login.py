from auxiliares import mensajes
from auxiliares.configuracion import MAX_INTENTOS_LOGIN
from negocio.excepciones import NegocioError
from presentacion import consola as c


class PresentacionLogin:
    def __init__(self, servicio_usuarios):
        self._servicio = servicio_usuarios

    def _crear_primer_usuario(self):
        print("\nNo hay usuarios registrados. Crea la cuenta inicial para comenzar.")
        while True:
            try:
                nombre = c.leer("Nombre: ")
                correo = c.leer("Correo: ")
                clave = c.leer_contrasena_nueva("Contraseña: ")
                usuario = self._servicio.crear(nombre, correo, clave)
                print(f"  ✔ Cuenta creada: {usuario.describir()}")
                return
            except (ValueError, NegocioError) as e:
                print(f"  ⚠ {e}")

    def iniciar_sesion(self):
        """Devuelve el Usuario autenticado, o None si se cancela o se agotan los intentos."""
        if not self._servicio.hay_usuarios():
            self._crear_primer_usuario()
        print("\n--- INICIO DE SESIÓN (deja el correo vacío para salir) ---")
        for _ in range(MAX_INTENTOS_LOGIN):
            correo = c.leer("Correo: ")
            if not correo:
                return None
            clave = c.leer_contrasena("Contraseña: ")
            try:
                usuario = self._servicio.autenticar(correo, clave)
            except NegocioError as e:
                print(f"  ⚠ {e}")
                continue
            print(f"\n  ✔ Bienvenido/a, {usuario.nombre}.")
            return usuario
        print(f"  ⚠ {mensajes.SIN_INTENTOS}")
        return None
