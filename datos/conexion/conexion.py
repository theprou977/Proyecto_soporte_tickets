import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, event, text

RAIZ = Path(__file__).resolve().parents[2]  # carpeta raíz del proyecto
load_dotenv(RAIZ / ".env")


class Conexion:
    """Singleton que administra el engine de SQLAlchemy."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._iniciar()
        return cls._instancia

    def _iniciar(self):
        url = os.getenv("DATABASE_URL", "sqlite:///soporte.db")
        self._engine = create_engine(url)
        if url.startswith("sqlite"):
            @event.listens_for(self._engine, "connect")
            def _fk(dbapi_con, _):
                dbapi_con.execute("PRAGMA foreign_keys=ON")

    @property
    def engine(self):
        return self._engine

    def ejecutar_script(self, ruta):
        """Ejecuta un archivo .sql (sentencias separadas por ';')."""
        contenido = Path(ruta).read_text(encoding="utf-8")
        with self._engine.begin() as con:
            for sentencia in contenido.split(";"):
                if sentencia.strip():
                    con.execute(text(sentencia))

    def inicializar_bd(self):
        self.ejecutar_script(RAIZ / "datos" / "sql" / "schema.sql")
