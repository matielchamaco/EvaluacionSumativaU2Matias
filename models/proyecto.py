from datetime import datetime

class Proyecto:

    def __init__(
            self, id_proyecto: int, nombre: str, fecha_inicio: datetime
    ):

        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._fecha_inicio = fecha_inicio

    @property
    def id_proyecto(self) -> int:
        return self._id_proyecto

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def id_proyecto(self) -> int:
        return self._id_gerente

    @id_proyecto.setter
    def id_proyecto(self, valor: int):
        self._id_gerente = valor

    def __str__(self) -> str:
        proyecto_info = (
        self._id_empleado
        if self._id_empleado is not None
        else "Proyecto sin empleados asignados"
    )
        return f"Departamento [{self._id_proyecto}]: {self._nombre} (ID Gerente: {proyecto_info})"