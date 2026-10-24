import sys
# Importación de clases previas
from models.entidades import Empleado, Departamento
from config.db_manager import DatabaseManager
from helper.input_helpers import leer_entero, leer_flotante, leer_texto, leer_rut

class MenuApp:
    """Controla el flujo de navegación del sistema de gestión por consola."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def mostrar_menu_principal(self):
        while True:
            print("\n==============================================")
            print("    ECOTECH SOLUTIONS - SISTEMA DE GESTIÓN   ")
            print("==============================================")
            print("1. Gestión de Empleados")
            print("2. Gestión de Departamentos")
            print("0. Salir del Sistema")
            print("----------------------------------------------")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._menu_empleados()
            elif opcion == "2":
                self._menu_departamentos()
            elif opcion == "0":
                print("\nGracias por utilizar el sistema de EcoTech Solutions. ¡Hasta luego! :)")
                sys.exit(0)
            else:
                print("Opción no válida. Intente nuevamente.")

    # --------------------------------------------------
    # SUBMENÚ: GESTIÓN DE EMPLEADOS
    # --------------------------------------------------

    def _menu_empleados(self):
        while True:
            print("\n--- GESTIÓN DE EMPLEADOS ---")
            print("1. Registrar nuevo empleado")
            print("2. Listar todos los empleados")
            print("3. Buscar empleado por ID")
            print("4. Actualizar empleado (Nombre/Salario)")
            print("5. Eliminar empleado")
            print("0. Volver al menú principal")

            opcion = input("Opción: ").strip()

            if opcion == "1":
                self._registrar_empleado()
            elif opcion == "2":
                self._listar_empleados()
            elif opcion == "3":
                self._buscar_empleado()
            elif opcion == "4":
                self._actualizar_empleado()
            elif opcion == "5":
                self._eliminar_empleado()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    def _registrar_empleado(self):
        print("\n[ Registrar Empleado ]")
        id_emp = leer_entero("Ingrese ID del empleado (entero positivo): ", minimo=1)
        nombre = leer_texto("Ingrese nombre completo: ")
        rut = leer_rut("Ingrese RUT (ej: 12.345.678-9): ")
        salario = leer_flotante("Ingrese salario mensual ($): ", minimo=0.0)

        nuevo_emp = Empleado(id_empleado=id_emp, nombre=nombre, rut=rut, salario=salario)
        self.db.crear_empleado(nuevo_emp)

    def _listar_empleados(self):
        print("\n[ Nómina de Empleados Registrados ]")
        empleados = self.db.listar_empleados()
        if not empleados:
            print("No existen empleados registrados actualmente.")
            return
        for emp in empleados:
            print(emp)

    def _buscar_empleado(self):
        print("\n[ Buscar Empleado ]")
        id_emp = leer_entero("Ingrese el ID del empleado a buscar: ", minimo=1)
        emp = self.db.obtener_empleado_por_id(id_emp)
        if emp:
            print(f"\nRegistro encontrado: {emp}")
        else:
            print(f"No existe un empleado registrado con el ID {id_emp}.")

    def _actualizar_empleado(self):
        print("\n[ Actualizar Datos de Empleado ]")
        id_emp = leer_entero("Ingrese ID del empleado a actualizar: ", minimo=1)
        emp = self.db.obtener_empleado_por_id(id_emp)

        if not emp:
            print(f"No existe un empleado con ID {id_emp}.")
            return

        print(f"Empleado seleccionado: {emp.nombre} - Salario actual: ${emp.salario:,.2f}")
        nuevo_nombre = input("Ingrese nuevo nombre (dejar en blanco para mantener el actual): ").strip()
        nuevo_salario_str = input("Ingrese nuevo salario (dejar en blanco para mantener el actual): ").strip()

        if nuevo_nombre:
            emp.nombre = nuevo_nombre
        if nuevo_salario_str:
            try:
                emp.salario = float(nuevo_salario_str)
            except ValueError:
                print("Monto inválido. El salario no fue modificado.")

        self.db.actualizar_empleado(emp)

    def _eliminar_empleado(self):
        print("\n[ Eliminar Registro de Empleado ]")
        id_emp = leer_entero("Ingrese ID del empleado a eliminar: ", minimo=1)
        confirmacion = input(f"¿Está seguro de eliminar al empleado ID {id_emp}? (s/n): ").strip().lower()

        if confirmacion == "s":
            self.db.eliminar_empleado(id_emp)
        else:
            print("Operación cancelada.")

    # --------------------------------------------------
    # SUBMENÚ: GESTIÓN DE DEPARTAMENTOS
    # --------------------------------------------------
    
    def _menu_departamentos(self):
        while True:
            print("\n--- GESTIÓN DE DEPARTAMENTOS ---")
            print("1. Registrar nuevo departamento")
            print("2. Listar departamentos")
            print("0. Volver al menú principal")

            opcion = input("Opción: ").strip()

            if opcion == "1":
                self._registrar_departamento()
            elif opcion == "2":
                self._listar_departamentos()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    def _registrar_departamento(self):
        print("\n[ Registrar Departamento ]")
        id_depto = leer_entero("Ingrese ID del departamento: ", minimo=1)
        nombre = leer_texto("Ingrese nombre del departamento: ")

        asignar = input("¿Desea asignar un gerente existente? (s/n): ").strip().lower()
        id_gerente = None
        if asignar == "s":
            id_gerente = leer_entero("Ingrese ID del empleado gerente: ", minimo=1)

        depto = Departamento(id_departamento=id_depto, nombre=nombre, id_gerente=id_gerente)
        self.db.crear_departamento(depto)

    def _listar_departamentos(self):
        print("\n[ Lista de Departamentos ]")
        deptos = self.db.listar_departamentos()
        if not deptos:
            print("No hay departamentos registrados.")
            return
        for d in deptos:
            print(d)