import fitz  # PyMuPDF

def extract_rut_data_reordered(pdf_path):
    """
    Extracción refinada de nombres y cédulas en todas las páginas del documento RUT.
    Se optimiza la detección de nombres asegurando que primero aparecen los nombres y luego los apellidos.
    """
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        text_lines = page.get_text("text").split("\n")

        name = None
        id_number = None

        # Buscar el nombre en cualquier parte de la página con una estrategia más flexible
        for i in range(len(text_lines) - 1):
            line = text_lines[i].strip().upper()
            next_line = text_lines[i + 1].strip().upper() if i + 1 < len(text_lines) else ""

            # Si encontramos un nombre completo (mínimo 3 palabras) antes de "CONTRIBUYENTE"
            words = line.split()
            if len(words) >= 3 and "CONTRIBUYENTE" in next_line:
                # Reorganizar: las primeras dos palabras como apellidos, el resto como nombres
                name = " ".join(words[2:]) + " " + " ".join(words[:2])
                break

        # Mantener la lógica de extracción de cédulas ya funcional
        for i in range(len(text_lines) - 1):
            if "CÉDULA DE CIUDADANÍA" in text_lines[i].strip().upper():
                for j in range(i + 1, min(i + 5, len(text_lines))):  # Buscar en las siguientes líneas
                    potential_id = text_lines[j].strip().replace(" ", "").replace(".", "").replace(",", "")
                    if potential_id.isdigit() and 6 <= len(potential_id) <= 10:  # Filtrar por longitud esperada
                        id_number = potential_id
                        break

        # Guardar los datos si se encontraron valores válidos
        if name and id_number:
            extracted_data.append({"Página": page_num, "Nombre": name, "Cédula": id_number})

    return extracted_data
