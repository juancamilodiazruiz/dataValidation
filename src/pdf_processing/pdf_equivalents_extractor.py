import fitz  # PyMuPDF
import re

def extract_equivalents_data(pdf_path):
    """
    Extrae nombres completos y números de cédula desde el documento PDF de equivalentes.
    Se ajusta la lógica para capturar correctamente los valores basados en la estructura real del documento.
    """
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").upper()
        text_lines = text.split("\n")

        name, id_number = None, None

        for i in range(len(text_lines) - 1):
            # Buscar el nombre del proveedor: Aparece justo después de la comercializadora
            if "DIRECCIÓN:" in text_lines[i] and i + 1 < len(text_lines):
                name = text_lines[i + 1].strip()  # La siguiente línea contiene el nombre

            # Buscar la cédula del proveedor: Aparece después de la fecha
            if "DSNO" in text_lines[i]:
                for j in range(i + 4, min(i + 8, len(text_lines))):  # Buscar en las siguientes líneas
                    potential_id = text_lines[j].strip().replace(".", "").replace(",", "")
                    if potential_id.isdigit() and len(potential_id) > 5:  # Verificar que sea un número válido
                        id_number = potential_id
                        break

            # Si ambos valores se encontraron, guardarlos y continuar
            if name and id_number:
                extracted_data.append({"Página": page_num, "Nombre": name, "Cédula": id_number})
                name, id_number = None, None  # Reset para evitar duplicados

    return extracted_data
