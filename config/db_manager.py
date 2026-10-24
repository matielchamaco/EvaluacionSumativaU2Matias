import sqlite3
from typing import List, Optional
# Importamos las clases definidas anteriormente
from models.entidades import Empleado, Departamento

class DatabaseManager:
    """Clase encargada de gestionar la conexión y operaciones CRUD en SQLite de manera segura."""

    def __init__(self, db_name: str = "empresa.db"):
        self.db_name = db_name
        self._inicializar_tablas()

    def _obtener_conexion(self) -> sqlite3.Connection:
        """Establece y retorna una conexión a la base de datos."""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")  # Habilita claves foráneas
        return conn

    def _inicializar_tablas(self):
        """Crea las tablas necesarias en la base de datos si no existen."""
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()

                # Tabla Departamento
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS departamentos (
                        id_departamento INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        id_gerente INTEGER
                    );
                """
                )

                # Tabla Empleado
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS empleados (
                        id_empleado INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        rut TEXT UNIQUE NOT NULL,
                        salario REAL NOT NULL
                    );
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR DB] Fallo al inicializar la base de datos: {e}")

    # ------------------------------------------
    # --- CRUD EMPLEADOS ---
    # ------------------------------------------

    def crear_empleado(self, emp: Empleado) -> bool:
        """Inserta un nuevo empleado utilizando consultas parametrizadas."""
        sql = "INSERT INTO empleados (id_empleado, nombre, rut, salario) VALUES (?, ?, ?, ?)"
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql, (emp.id_empleado, emp.nombre, emp.rut, emp.salario)
                )
                conn.commit()
                print(f"Empleado '{emp.nombre}' registrado exitosamente.")
                return True
        except sqlite3.IntegrityError:
            print(
                f"[ERROR] El ID {emp.id_empleado} o RUT '{emp.rut}' ya está registrado."
            )
            return False
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al registrar empleado: {e}")
            return False

    def obtener_empleado_por_id(
        self, id_empleado: int
    ) -> Optional[Empleado]:
        """Consulta un empleado por su ID."""
        sql = "SELECT id_empleado, nombre, rut, salario FROM empleados WHERE id_empleado = ?"
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (id_empleado,))
                row = cursor.fetchone()
                if row:
                    return Empleado(
                        id_empleado=row[0],
                        nombre=row[1],
                        rut=row[2],
                        salario=row[3],
                    )
                return None
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al consultar empleado: {e}")
            return None

    def listar_empleados(self) -> List[Empleado]:
        """Retorna la lista completa de empleados registrados."""
        sql = "SELECT id_empleado, nombre, rut, salario FROM empleados"
        empleados = []
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    empleados.append(
                        Empleado(
                            id_empleado=row[0],
                            nombre=row[1],
                            rut=row[2],
                            salario=row[3],
                        )
                    )
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al listar empleados: {e}")
        return empleados

    def actualizar_empleado(self, emp: Empleado) -> bool:
        """Actualiza el nombre y salario de un empleado existente."""
        sql = "UPDATE empleados SET nombre = ?, salario = ? WHERE id_empleado = ?"
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (emp.nombre, emp.salario, emp.id_empleado))
                conn.commit()
                if cursor.rowcount > 0:
                    print(
                        f"Empleado ID {emp.id_empleado} actualizado correctamente."
                    )
                    return True
                print(
                    f"[AVISO] No se encontró el empleado ID {emp.id_empleado} para actualizar."
                )
                return False
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al actualizar empleado: {e}")
            return False

    def eliminar_empleado(self, id_empleado: int) -> bool:
        """Elimina un empleado por su ID."""
        sql = "DELETE FROM empleados WHERE id_empleado = ?"
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (id_empleado,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Empleado ID {id_empleado} eliminado.")
                    return True
                print(
                    f"[AVISO] No se encontró el empleado ID {id_empleado}."
                )
                return False
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al eliminar empleado: {e}")
            return False

    # ------------------------------------------
    # --- CRUD DEPARTAMENTOS ---
    # ------------------------------------------

    def crear_departamento(self, depto: Departamento) -> bool:
        """Inserta un nuevo departamento."""
        sql = "INSERT INTO departamentos (id_departamento, nombre, id_gerente) VALUES (?, ?, ?)"
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql,
                    (
                        depto.id_departamento,
                        depto.nombre,
                        depto.id_gerente,
                    ),
                )
                conn.commit()
                print(
                    f"Departamento '{depto.nombre}' registrado exitosamente."
                )
                return True
        except sqlite3.IntegrityError:
            print(
                f"[ERROR] El departamento ID {depto.id_departamento} ya existe."
            )
            return False
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al crear departamento: {e}")
            return False

    def listar_departamentos(self) -> List[Departamento]:
        """Consulta todos los departamentos almacenados."""
        sql = "SELECT id_departamento, nombre, id_gerente FROM departamentos"
        deptos = []
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    deptos.append(
                        Departamento(
                            id_departamento=row[0],
                            nombre=row[1],
                            id_gerente=row[2],
                        )
                    )
        except sqlite3.Error as e:
            print(f"[ERROR DB] Error al listar departamentos: {e}")
        return deptos