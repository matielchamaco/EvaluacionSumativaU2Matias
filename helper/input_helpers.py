import re

def leer_entero(mensaje: str, minimo: int = None) -> int:
    """Solicita un número entero por consola de forma segura con try-except."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error de entrada: Por favor, ingresa un número entero válido.")

def leer_flotante(mensaje: str, minimo: float = 0.0) -> float:
    """Solicita un número decimal de forma segura, validando un mínimo permitido."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                print(f"Error: El monto no puede ser inferior a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error de entrada: Por favor, ingresa un número decimal válido.")

def leer_texto(mensaje: str) -> str:
    """Solicita un texto asegurando que no quede vacío ni compuesto solo por espacios."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Error: Este campo no puede quedar vacío.")

import re

def validar_rut(rut: str) -> bool:
    """Valida que el RUT tenga una longitud de entre 7 y 9 caracteres válidos

    (cuerpo numérico y dígito verificador 0-9 o K).
    """
    if not rut or not isinstance(rut, str):
        return False

    # Limpiar puntos, guiones y espacios
    rut_limpio = re.sub(r"[^\dKk]", "", rut).upper()

    # Permitir de 7 a 9 caracteres (ej: 6 dígitos + DV hasta 8 dígitos + DV)
    if len(rut_limpio) < 7 or len(rut_limpio) > 9:
        return False

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    # Validar que el cuerpo sean números y el DV sea dígito o 'K'
    return cuerpo.isdigit() and (dv.isdigit() or dv == "K")

def leer_rut(mensaje: str) -> str:
    """Solicita un RUT por consola y repite hasta que el RUT sea válido."""
    while True:
        rut_input = input(mensaje).strip()
        if validar_rut(rut_input):
            rut_clean = re.sub(r"[^\dKk]", "", rut_input).upper()
            return f"{rut_clean[:-1]}-{rut_clean[-1]}"
        print(
            "⚠️  RUT inválido. Debe contener entre 7 y 8 dígitos más dígito verificador correcto (ej: 12.345.678-9)."
        )

