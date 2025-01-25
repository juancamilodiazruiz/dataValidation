import re

def parse_dni_data(text):
    """
    Extrae datos relevantes de un texto (e.g., DNI y nombre).
    :param text: Texto extraído por OCR.
    :return: Diccionario con datos extraídos.
    """
    dni_pattern = r"\b\d{8}\b"  # Ajustar según el formato
    name_pattern = r"Nombre: (.+)"  # Ajustar según el formato del DNI

    dni = re.search(dni_pattern, text)
    name = re.search(name_pattern, text)

    return {
        "dni": dni.group(0) if dni else None,
        "name": name.group(1) if name else None
    }
