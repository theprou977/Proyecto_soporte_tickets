# Sistema de Tickets de Soporte

Proyecto de **Programación Orientada a Objetos** (Evaluación N°3), desarrollado en Python con arquitectura multicapa, ORM Peewee y MySQL.

## Integrantes
- Francisco Valle
- Tomas Muñoz

## Descripción general
Aplicación de consola para gestionar el soporte técnico de una organización. Permite administrar **usuarios**, **técnicos**, **tickets** y **acciones de soporte** (historial de cada ticket), con CRUD completo de cada entidad.

Es la continuación del proyecto de la Evaluación N°2: se conservan el diagrama de clases, el modelo de datos, los scripts SQL, la conexión a la base de datos y el archivo `.env`. En esta evaluación se agregó:
- Modelos y repositorios con el ORM **Peewee** (conexión a MySQL).
- **Login obligatorio**: no se puede acceder al menú sin iniciar sesión.
- Contraseñas **ocultas al escribirlas** (Maskpass) y **protegidas con hash** (Bcrypt).

Reglas de negocio principales:
- Flujo de estados del ticket: Abierto → Asignado → EnProceso → Resuelto → Cerrado (transiciones validadas).
- Solo el técnico asignado puede registrar acciones en un ticket.
- No se elimina un usuario con tickets, ni un técnico con tickets en curso o acciones registradas.
- Un usuario no puede eliminar su propia cuenta con la sesión abierta.

## Arquitectura
```
├── main.py / app.py               # inicio de la app (llama primero al login)
├── requirements.txt
├── .env.example                   # plantilla del archivo de ambiente
├── diagrama_clases.png            # diagrama de clases (UML)
├── auxiliares/                    # validaciones, mensajes y configuración
│   ├── configuracion.py  info_app.py  mensajes.py  opciones_menu.py
│   ├── validaciones.py  fechas.py
│   └── seguridad.py               # hash y verificación con Bcrypt
├── datos/                         # persistencia
│   ├── conexion_db.py             # conexión Peewee + ejecución de scripts SQL
│   ├── modelos/                   # models.py (ModelBase), persona, usuario, tecnico,
│   │                              # ticket, accion_soporte, enums
│   ├── repositorios/              # repo_base + repo_usuario, repo_tecnico,
│   │                              # repo_ticket, repo_accion (CRUD de cada modelo)
│   └── sql/                       # scripts de creación de la base de datos
├── negocio/                       # reglas del sistema y procesamiento de datos
└── presentacion/                  # interacción con el usuario (menús y login)
```
Flujo entre capas: `presentacion → negocio → datos`.

## Dependencias
Requiere **Python 3.10 o superior** y un servidor **MySQL / MariaDB** en ejecución.

| Librería | Uso |
|---|---|
| `peewee` | ORM (modelos y repositorios) |
| `PyMySQL` | driver de MySQL para Peewee |
| `bcrypt` | hash de contraseñas |
| `maskpass` | ocultar la contraseña al escribirla |
| `python-decouple` | leer el archivo `.env` |
| `prettytable` | tablas en consola |

## Procedimiento de instalación
1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crear un usuario de MySQL para el proyecto (en phpMyAdmin o en el cliente `mysql`):
   ```sql
   CREATE USER 'pancho'@'localhost' IDENTIFIED BY '1234';
   GRANT ALL PRIVILEGES ON soporte_tickets.* TO 'pancho'@'localhost';
   FLUSH PRIVILEGES;
   ```
   (Puede usarse otro nombre y clave, o `root`; deben coincidir con el `.env`.)
5. Crear el archivo `.env` a partir de la plantilla (`copy .env.example .env` en Windows, `cp .env.example .env` en Linux/Mac) y completarlo:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=pancho
   DB_PASSWORD=1234
   DB_NAME=soporte_tickets
   ```
   El usuario de MySQL debe tener permisos sobre la base indicada en `DB_NAME`.

## Procedimiento de creación de base de datos
**Automático (recomendado):** al ejecutar `python main.py`, el programa crea la base de datos indicada en `DB_NAME` si no existe y ejecuta, en orden cronológico, los scripts de `datos/sql/`:
1. `2026.11.21_10.00_DDL_soporte.sql`: crea las tablas `usuarios`, `tecnicos`, `tickets` y `acciones_soporte`.
2. `2026.11.21_10.05_ALTER_usuarios_contrasena.sql`: agrega a `usuarios` la columna `contrasena` (hash Bcrypt).

Los scripts pueden ejecutarse varias veces sin error.

**Manual (opcional):** desde phpMyAdmin o el cliente de MySQL:
```sql
CREATE DATABASE soporte_tickets CHARACTER SET utf8mb4;
USE soporte_tickets;
-- ejecutar, en el orden indicado arriba, los archivos de datos/sql/
```

## Usuario inicial
Correo: francisco@gmail.com
contraseña:francisco1

Luego se inicia sesión con ese correo y esa contraseña. Desde el menú **Usuarios** se pueden crear más usuarios.

## Instrucciones de ejecución
Con el entorno virtual activo y MySQL encendido:
```bash
python main.py
```
(`python app.py` hace lo mismo.)

1. Iniciar sesión con correo y contraseña (3 intentos; dejar el correo vacío para salir).
2. En el menú principal elegir **Usuarios**, **Técnicos**, **Tickets** o **Acciones de soporte**; cada módulo tiene su CRUD.
3. Flujo típico: crear un técnico → crear un ticket para un usuario → «Atender» (el técnico toma el ticket) → registrar acciones → cambiar el estado hasta cerrarlo.
4. Con la opción `0` del menú principal se cierra la sesión y se vuelve al login.

## Seguridad
- Las contraseñas se piden con **Maskpass** (se muestran como `*`) y se guardan como **hash Bcrypt** en la columna `usuarios.contrasena`; nunca en texto plano.
- El login muestra el mismo mensaje si falla el correo o la contraseña.
- El archivo `.env` (con las credenciales de MySQL) no se sube al repositorio; se incluye `.env.example` como plantilla.

## Principios de POO aplicados
- **Herencia:** `Usuario` y `Tecnico` heredan de `Persona`; todos los modelos heredan de `ModelBase`.
- **Polimorfismo:** `rol()` y `describir()` cambian según la subclase; los 4 repositorios cumplen el mismo contrato (`crear`, `obtener`, `listar`, `actualizar`, `eliminar`).
- **Abstracción:** `RepositorioBase` es una clase abstracta (ABC).
- **Encapsulamiento:** el estado del ticket solo cambia con `cambiar_estado()`, que valida las transiciones.