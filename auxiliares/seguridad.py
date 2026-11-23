"""Hash y verificación de contraseñas con Bcrypt."""
import bcrypt

_hash_falso = None


def hashear(contrasena):
    """Devuelve el hash bcrypt (60 caracteres) listo para guardar en la BD."""
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verificar(contrasena, hash_guardado):
    if not hash_guardado:
        return False
    try:
        return bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("ascii"))
    except ValueError:  # contraseña > 72 bytes o hash corrupto
        return False


def verificacion_falsa(contrasena):
    """Gasta el mismo tiempo que una verificación real cuando el correo no existe,
    para que no se pueda adivinar qué correos están registrados."""
    global _hash_falso
    if _hash_falso is None:
        _hash_falso = hashear("contrasena-falsa-1")
    verificar(contrasena, _hash_falso)
    return False
