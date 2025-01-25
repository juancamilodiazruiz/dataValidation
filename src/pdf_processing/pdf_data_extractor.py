import fitz  # PyMuPDF
import re
from datetime import datetime

# Expresiones regulares para extraer información
name_pattern = re.compile(r"QUE EL SEÑOR\(A\)?\s*([A-ZÁÉÍÓÚÑ ]{5,})\s*IDENTIFICADO", re.IGNORECASE)
id_pattern = re.compile(r"(?:NÚMERO DE DOCUMENTO|IDENTIFICADO CON EL NÚMERO|DOCUMENTO DE IDENTIDAD)[:]? ([\d\.,]+)", re.IGNORECASE)
date_pattern = re.compile(r"VIGENCIA DE UN AÑO, HASTA EL (\d{1,2} DE [A-ZÁÉÍÓÚÑ]+ DE \d{4})", re.IGNORECASE)

# Mapeo de nombres de meses en español a números
month_mapping = {
    "ENERO": "01", "FEBRERO": "02", "MARZO": "03", "ABRIL": "04",
    "MAYO": "05", "JUNIO": "06", "JULIO": "07", "AGOSTO": "08",
    "SEPTIEMBRE": "09", "OCTUBRE": "10", "NOVIEMBRE": "11", "DICIEMBRE": "12"
}

def parse_date(date_str):
    """
    Convierte una fecha en formato '11 de Julio de 2025' a un objeto datetime correctamente.
    """
    try:
        parts = date_str.strip().split(" DE ")
        if len(parts) != 3:
            raise ValueError("Formato de fecha inesperado")

        day = int(parts[0].strip())
        month_name = parts[1].strip().upper()
        year = int(parts[2].strip())

        month = month_mapping.get(month_name, None)
        if not month:
            raise ValueError(f"Mes desconocido: {month_name}")

        formatted_date = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
        return formatted_date
    except Exception as e:
        print(f"Error al convertir la fecha '{date_str}': {e}")  # Debugging
        return None

def clean_text(text):
    """
    Normaliza el texto eliminando espacios innecesarios y convirtiéndolo a mayúsculas.
    """
    text = text.upper()
    text = re.sub(r"\s+", " ", text)  # Reemplaza múltiples espacios con uno solo
    return text.strip()

def extract_data_from_pdf(pdf_path):
    """
    Extrae información de cada página del PDF y la procesa en un diccionario.

    :param pdf_path: Ruta del archivo PDF.
    :return: Lista de diccionarios con los datos extraídos de cada página.
    """
    doc = fitz.open(pdf_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        text = clean_text(page.get_text("text"))  # Normalizar el texto

        # Extraer datos con regex mejorada
        name_match = name_pattern.search(text)
        id_match = id_pattern.search(text)
        date_match = date_pattern.search(text)

        name = name_match.group(1).strip() if name_match else "No encontrado"
        id_number = id_match.group(1).strip() if id_match else "No encontrado"
        expiry_date_str = date_match.group(1).strip() if date_match else "No encontrada"

        # Normalizar el formato de la cédula (eliminar comas o puntos innecesarios)
        id_number = id_number.replace(",", "").replace(".", "")

        # Validar fecha de vencimiento
        expiry_date_valid = False
        if expiry_date_str != "No encontrada":
            expiry_date = parse_date(expiry_date_str)
            if expiry_date:
                expiry_date_valid = expiry_date >= datetime.today()

        # Almacenar resultado en una estructura de datos
        results.append({
            "Página": page_num,
            "Nombre": name,
            "Cédula": id_number,
            "Fecha de Vencimiento": expiry_date_str,
            "Fecha Válida": "Sí" if expiry_date_valid else "No"
        })

    return results
