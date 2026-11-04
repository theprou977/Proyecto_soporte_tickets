from abc import ABC, abstractmethod

from sqlalchemy import text

from datos.conexion.conexion import Conexion


class RepositorioBase(ABC):
    """Contrato CRUD; cada repositorio concreto lo implementa (polimorfismo)."""

    def __init__(self, conexion=None):
        self._conexion = conexion or Conexion()

    @abstractmethod
    def crear(self, entidad): ...

    @abstractmethod
    def obtener(self, id): ...

    @abstractmethod
    def listar(self): ...

    @abstractmethod
    def actualizar(self, entidad): ...

    @abstractmethod
    def eliminar(self, id): ...

    def _escribir(self, sql, params=None):
        with self._conexion.engine.begin() as con:
            return con.execute(text(sql), params or {})

    def _leer(self, sql, params=None):
        with self._conexion.engine.connect() as con:
            return con.execute(text(sql), params or {}).mappings().all()
