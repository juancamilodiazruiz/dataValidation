import fitz  # PyMuPDF
import re

def extract_names_and_ids(pdf_path):
    """
    Extrae nombres completos y números de cédula del archivo PDF de declaración de producción,
    asegurando que los datos en las últimas líneas de cada página sean capturados correctamente.
    """
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").upper()  # Convertir todo a mayúsculas para uniformidad
        text_lines = text.split("\n")

        # Patrón principal para nombres y cédulas en la estructura estándar
        matches = re.findall(r"([A-ZÁÉÍÓÚÑ]+(?:\s[A-ZÁÉÍÓÚÑ]+)*)\n([A-ZÁÉÍÓÚÑ]+(?:\s[A-ZÁÉÍÓÚÑ]+)*)\n([\d\.,]+)", text)

        for match in matches:
            full_name = f"{match[0]} {match[1]}".strip()
            id_number = match[2].replace(".", "").strip()

            if id_number.isdigit() and 6 <= len(id_number) <= 10:
                extracted_data.append({"Página": page_num, "Nombre": full_name, "Cédula": id_number})

        # Revisión especial para capturar nombres y cédulas en las últimas líneas de la página
        last_lines = text_lines[-10:]  # Analizar solo las últimas 10 líneas

        for i in range(len(last_lines) - 2):
            name = last_lines[i].strip()
            surname = last_lines[i + 1].strip()
            id_number = last_lines[i + 2].replace(".", "").strip()

            if name.isalpha() and surname.isalpha() and id_number.isdigit():
                extracted_data.append({"Página": page_num, "Nombre": f"{name} {surname}", "Cédula": id_number})

    return extracted_data
