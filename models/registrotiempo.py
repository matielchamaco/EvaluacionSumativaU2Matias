from datetime import datetime

class Proyecto:

    def __init__(
            self, id_registro: int, horas: float, fecha: datetime
    ):

        self._id_registro = id_registro
        self._horas = horas
        self._fecha = fecha