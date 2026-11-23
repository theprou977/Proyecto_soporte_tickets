# Sistema de Tickets de Soporte (POO en Python)

Evaluación N°3 – Programación Orientada a Objetos. Continuación del proyecto de la
Evaluación N°2: se conserva el diagrama de clases, el modelo de datos (ahora con el ORM
**Peewee**), los scripts SQL, la conexión a la base de datos y el archivo de ambiente `.env`.
Se agregó **CRUD completo en repositorios**, **login obligatorio**, **contraseñas ocultas con
Maskpass** y **contraseñas protegidas con hash Bcrypt**.

## Dependencias
| Librería | Uso |
|---|---|
| `peewee` | ORM (modelos y repositorios) |
| `PyMySQL` | driver de MySQL para Peewee |
| `bcrypt` | hash de contraseñas |
| `maskpass` | ocultar la contraseña al escribirla |
| `python-decouple` | leer el archivo `.env` |
| `prettytable` | tablas en consola |

Requiere Python 3.10+ y un servidor MySQL (o MariaDB) en ejecución.

## Instalación y ejecución
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env  → editar con tus datos de MySQL
python main.py
```
`main.py` crea la base de datos si no existe, ejecuta los scripts de `datos/sql/` en orden
(se pueden ejecutar varias veces sin error) y **parte siempre con el login**. `app.py` es un
atajo que hace lo mismo.

**Primer uso:** si no hay usuarios registrados, el sistema pide crear la cuenta inicial
(nombre, correo y contraseña). Después hay que iniciar sesión con ella.

### Variables de `.env`
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_clave
DB_NAME=soporte_tickets
```

### Crear la base de datos a mano (opcional)
```sql
CREATE DATABASE soporte_tickets CHARACTER SET utf8mb4;
USE soporte_tickets;
-- luego ejecutar, en este orden, los archivos de datos/sql/
```

## Estructura
```
├── diagrama_clases.png            # UML de la Evaluación 2
├── main.py / app.py               # inicio de la app (llama primero al login)
├── .env.example                   # plantilla del archivo de ambiente
├── requirements.txt
├── auxiliares/                    # validaciones, mensajes y configuración
│   ├── configuracion.py           #   lee .env
│   ├── info_app.py  mensajes.py  opciones_menu.py
│   ├── validaciones.py            #   texto, correo, contraseña
│   ├── seguridad.py               #   hash y verificación con Bcrypt
│   └── fechas.py
├── datos/                         # persistencia
│   ├── conexion_db.py             #   objeto de BD de Peewee + ejecución de scripts
│   ├── modelos/                   #   models.py (ModelBase), persona, usuario, tecnico,
│   │                              #   ticket, accion_soporte, enums
│   ├── repositorios/              #   repo_base (abstracto) + repo_usuario, repo_tecnico,
│   │                              #   repo_ticket, repo_accion  → CRUD de cada modelo
│   └── sql/                       #   scripts de creación (DDL) y ALTER de usuarios
├── negocio/                       # reglas del sistema (negocio_usuarios, _tecnicos,
│                                  #   _tickets, _acciones, excepciones)
└── presentacion/                  # interacción con el usuario
    ├── menu.py                    #   menú principal (solo tras el login)
    └── presentacion_login / _usuario / _tecnico / _ticket / _accion .py
```
Flujo: `presentacion → negocio → datos`. La capa de presentación no habla con la BD.

## Seguridad
- Las contraseñas se piden con **Maskpass** (se ven como `*`) y se guardan como **hash Bcrypt**
  (columna `usuarios.contrasena`, 60 caracteres); nunca en texto plano.
- Requisitos: mínimo 8 caracteres, con al menos una letra y un número (máx. 72 bytes, límite de Bcrypt).
- El login muestra el mismo mensaje si falla el correo o la contraseña, y permite 3 intentos.
- No se puede entrar al menú sin sesión iniciada; "Cerrar sesión" vuelve al login.
- Un usuario no puede eliminar su propia cuenta mientras está conectado.

## Principios POO aplicados
- **Herencia:** `Usuario` y `Tecnico` heredan de `Persona`; todos los modelos heredan de `ModelBase`.
- **Polimorfismo:** `rol()` / `describir()` cambian según la subclase; los 4 repositorios
  implementan el mismo contrato `RepositorioBase` (`crear/obtener/listar/actualizar/eliminar`).
- **Encapsulamiento:** el estado del ticket solo cambia con `cambiar_estado()` (transiciones validadas);
  el hash se calcula únicamente en `seguridad.py`.
- **Abstracción:** `RepositorioBase` es una clase abstracta (ABC).

## Reglas de negocio
- Flujo de estados: Abierto → Asignado → EnProceso → Resuelto → Cerrado.
- Solo el técnico asignado registra acciones.
- No se elimina un usuario con tickets, ni un técnico con tickets en curso o acciones registradas.
- Al eliminar un ticket se elimina su historial de acciones (`ON DELETE CASCADE`).
