from abc import ABC, abstractmethod


class RepositorioBase(ABC):
    """Contrato CRUD; cada repositorio concreto lo implementa (polimorfismo)."""

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
