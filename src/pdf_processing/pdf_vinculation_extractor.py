import fitz  # PyMuPDF
import pandas as pd

def extract_vinculation_data(pdf_path):
    """
    Extrae nombres y números de cédula desde el documento PDF de vinculación.
    Se ajusta la lógica para capturar correctamente los valores basados en la estructura real del documento
    y evita la duplicación extrayendo solo una tupla por página.
    """
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        text_lines = text.split("\n")

        name, surname, id_number = None, None, None

        # Recorrer las líneas buscando los patrones adecuados
        for i in range(len(text_lines)):
            line = text_lines[i].strip()

            if line.isdigit() and len(line) >= 6:  # Detectar la cédula
                id_number = line

                # Buscar nombre y apellido en las líneas previas
                if i > 1:
                    surname = text_lines[i - 1].strip()
                    name = text_lines[i - 2].strip()

                # Asegurar que solo guardamos una vez por página
                if name and surname and id_number:
                    extracted_data.append({
                        "Página": page_num,
                        "Nombre_Vinculacion": f"{name} {surname}",
                        "Cédula_Vinculacion": id_number
                    })
                    break  # Salir del bucle para evitar múltiples capturas en una página

    # Convertir a DataFrame
    df_vinculacion = pd.DataFrame(extracted_data, columns=["Página", "Nombre_Vinculacion", "Cédula_Vinculacion"])

    return df_vinculacion
