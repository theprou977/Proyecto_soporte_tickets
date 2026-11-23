class NegocioError(Exception):
    """Error por incumplir una regla de negocio."""


class CredencialesInvalidas(NegocioError):
    """Correo o contraseña incorrectos (no distingue cuál, a propósito)."""
