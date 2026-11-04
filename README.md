# Sistema de Tickets de Soporte (POO en Python)

Evaluación 2 – Programación Orientada a Objeto Seguro. Arquitectura en 3 capas con consola.

## Estructura
```
IEC_N2_C2_POO/
├── diagrama_clases.png     # UML de la propuesta
├── app.py / main.py        # inicio de la app (menú CRUD)
├── datos/
│   ├── modelos/            # Persona (abstracta), Usuario, Tecnico, Ticket, AccionSoporte, enums
│   ├── repositorio/        # CRUD con SQL (RepositorioBase abstracto + 4 repos)
│   ├── conexion/           # Singleton con SQLAlchemy
│   ├── sql/schema.sql      # creación de tablas (se ejecuta al iniciar)
│   └── auxiliar/           # validaciones y fechas
├── negocio/                # servicios y reglas de negocio
└── presentacion/           # menú de consola
```

## Ejecución
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
La BD se configura en `.env` (`DATABASE_URL`, SQLite por defecto).

## Principios POO aplicados
- **Abstracción:** `Persona` y `RepositorioBase` son clases abstractas (ABC).
- **Encapsulamiento:** atributos privados (`_nombre`, `_estado`…) con `@property` y validación; el estado del ticket solo cambia con `cambiar_estado()`.
- **Herencia:** `Usuario` y `Tecnico` heredan de `Persona`; los repositorios heredan de `RepositorioBase`.
- **Polimorfismo:** `rol()`/`describir()` distintos según la subclase; todos los repos responden a `crear/obtener/listar/actualizar/eliminar`.

## Reglas de negocio
- Flujo de estados: Abierto → Asignado → EnProceso → Resuelto → Cerrado (transiciones validadas).
- Solo el técnico asignado registra acciones; no se elimina un usuario con tickets ni un técnico con tickets en curso.
