from helper.input_helpers import validar_rut
import re

class Empleado:

    def __init__(
        self, id_empleado: int, nombre: str, rut: str, salario: float | None = None
    ):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._rut = rut
        self.salario = salario  # Pasa por el setter para validar

    # --- Getters y Setters con Encapsulamiento ---

    @property
    def id_empleado(self) -> int:
        return self._id_empleado

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def rut(self) -> str:
        return self._rut

    @rut.setter
    def rut(self, valor: str):
        if not validar_rut(valor):
            raise ValueError(f"El RUT '{valor}' ingresado no es válido.")

        # Limpiamos y formateamos el RUT a '12345678-9'
        rut_limpio = re.sub(r"[^\dKk]", "", valor).upper()
        self._rut = f"{rut_limpio[:-1]}-{rut_limpio[-1]}"

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._salario = float(valor)

    def __str__(self) -> str:
        return f"Empleado [{self._id_empleado}]: {self._nombre} (RUT: {self._rut}) - Salario: ${self._salario:,.2f}"

class Departamento:

    def __init__(
        self, id_departamento: int, nombre: str, id_gerente: int = None
    ):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._id_gerente = id_gerente

    # --- Getters y Setters ---

    @property
    def id_departamento(self) -> int:
        return self._id_departamento

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def id_gerente(self) -> int:
        return self._id_gerente

    @id_gerente.setter
    def id_gerente(self, valor: int):
        self._id_gerente = valor

    def __str__(self) -> str:
        gerente_info = (
            self._id_gerente
            if self._id_gerente is not None
            else "Sin asignar"
        )
        return f"Departamento [{self._id_departamento}]: {self._nombre} (ID Gerente: {gerente_info})"