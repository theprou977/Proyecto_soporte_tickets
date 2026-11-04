from sqlalchemy.exc import SQLAlchemyError

from datos.modelos.enums import EstadoTicket, Prioridad, TipoAccion
from negocio.excepciones import NegocioError
from presentacion import consola as c


class Menu:
    def __init__(self, s_usuarios, s_tecnicos, s_tickets, s_acciones):
        self.su, self.st, self.sk, self.sa = s_usuarios, s_tecnicos, s_tickets, s_acciones

    def _submenu(self, titulo, opciones):
        """opciones: lista de (texto, funcion). Repite hasta elegir 0."""
        while True:
            print(f"\n=== {titulo} ===")
            for i, (txt, _) in enumerate(opciones, 1):
                print(f"{i}) {txt}")
            print("0) Volver")
            n = c.leer_entero("Opción: ")
            if n == 0:
                return
            if 1 <= n <= len(opciones):
                try:
                    opciones[n - 1][1]()
                except (ValueError, NegocioError) as e:
                    print(f"  ⚠ {e}")
                except SQLAlchemyError as e:
                    print(f"  ⚠ Error de base de datos: {e.__class__.__name__}")
                c.pausa()
            else:
                print("  ⚠ Opción inválida.")

    # ---- usuarios ----
    def usuarios(self):
        self._submenu("USUARIOS", [
            ("Crear", lambda: print("  ✔", self.su.crear(
                c.leer("Nombre: "), c.leer("Correo: ")).describir())),
            ("Listar", lambda: c.mostrar(self.su.listar())),
            ("Actualizar", lambda: print("  ✔", self.su.actualizar(
                c.leer_entero("ID: "), c.leer("Nuevo nombre: "), c.leer("Nuevo correo: ")).describir())),
            ("Eliminar", lambda: (self.su.eliminar(c.leer_entero("ID: ")), print("  ✔ Eliminado"))),
        ])

    # ---- técnicos ----
    def tecnicos(self):
        def carga():
            t = self.st.obtener(c.leer_entero("ID técnico: "))
            print(f"  {t.describir()} → carga de trabajo: {t.carga_trabajo()}")

        self._submenu("TÉCNICOS", [
            ("Crear", lambda: print("  ✔", self.st.crear(
                c.leer("Nombre: "), c.leer("Especialidad: ")).describir())),
            ("Listar", lambda: c.mostrar(self.st.listar())),
            ("Actualizar", lambda: print("  ✔", self.st.actualizar(
                c.leer_entero("ID: "), c.leer("Nuevo nombre: "), c.leer("Nueva especialidad: ")).describir())),
            ("Eliminar", lambda: (self.st.eliminar(c.leer_entero("ID: ")), print("  ✔ Eliminado"))),
            ("Ver carga de trabajo", carga),
        ])

    # ---- tickets ----
    def tickets(self):
        def crear():
            uid = c.leer_entero("ID usuario: ")
            desc = c.leer("Descripción: ")
            prio = c.elegir_enum(Prioridad, "Prioridad:")
            print("  ✔", self.sk.crear(uid, desc, prio).describir())

        def detalle():
            tid = c.leer_entero("ID ticket: ")
            print("  " + self.sk.obtener(tid).describir())
            print("  -- Historial de acciones --")
            c.mostrar(self.sk.historial(tid))

        def actualizar():
            tid = c.leer_entero("ID ticket: ")
            desc = c.leer("Nueva descripción: ")
            prio = c.elegir_enum(Prioridad, "Nueva prioridad:")
            print("  ✔", self.sk.actualizar(tid, desc, prio).describir())

        def asignar():
            t = self.sk.asignar(c.leer_entero("ID ticket: "), c.leer_entero("ID técnico: "))
            print("  ✔", t.describir())

        def atender():
            t = self.sk.atender(c.leer_entero("ID ticket: "), c.leer_entero("ID técnico: "))
            print("  ✔", t.describir())

        def estado():
            tid = c.leer_entero("ID ticket: ")
            nuevo = c.elegir_enum(EstadoTicket, "Nuevo estado:")
            print("  ✔", self.sk.cambiar_estado(tid, nuevo).describir())

        self._submenu("TICKETS", [
            ("Crear", crear),
            ("Listar", lambda: c.mostrar(self.sk.listar())),
            ("Ver detalle e historial", detalle),
            ("Actualizar descripción/prioridad", actualizar),
            ("Asignar técnico", asignar),
            ("Atender (técnico toma el ticket)", atender),
            ("Cambiar estado", estado),
            ("Eliminar", lambda: (self.sk.eliminar(c.leer_entero("ID: ")), print("  ✔ Eliminado"))),
        ])

    # ---- acciones ----
    def acciones(self):
        def registrar():
            tec = c.leer_entero("ID técnico: ")
            tic = c.leer_entero("ID ticket: ")
            desc = c.leer("Descripción: ")
            tipo = c.elegir_enum(TipoAccion, "Tipo de acción:")
            print("  ✔", self.sa.registrar(tec, tic, desc, tipo).describir())

        def actualizar():
            aid = c.leer_entero("ID acción: ")
            desc = c.leer("Nueva descripción: ")
            tipo = c.elegir_enum(TipoAccion, "Nuevo tipo:")
            print("  ✔", self.sa.actualizar(aid, desc, tipo).describir())

        self._submenu("ACCIONES DE SOPORTE", [
            ("Registrar", registrar),
            ("Listar", lambda: c.mostrar(self.sa.listar())),
            ("Actualizar", actualizar),
            ("Eliminar", lambda: (self.sa.eliminar(c.leer_entero("ID: ")), print("  ✔ Eliminada"))),
        ])

    def ejecutar(self):
        principal = {1: self.usuarios, 2: self.tecnicos, 3: self.tickets, 4: self.acciones}
        while True:
            print("\n===== SISTEMA DE TICKETS DE SOPORTE =====")
            print("1) Usuarios\n2) Técnicos\n3) Tickets\n4) Acciones de soporte\n0) Salir")
            n = c.leer_entero("Opción: ")
            if n == 0:
                print("¡Hasta luego!")
                return
            principal.get(n, lambda: print("  ⚠ Opción inválida."))()
