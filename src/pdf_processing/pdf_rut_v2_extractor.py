import fitz  # PyMuPDF
import pandas as pd
import re

def reorganize_name(full_name, second_surname):
    """
    Determina si el segundo apellido proporcionado realmente es un apellido o un primer nombre,
    basándose en la detección de doble espacio en el nombre original.

    :param full_name: String con el nombre desordenado (Apellidos primero, luego nombres).
    :param second_surname: String del posible segundo apellido.
    :return: True si es el segundo apellido, False si es el primer nombre.
    """
    # Eliminar espacios extra en los extremos
    full_name = full_name.strip()

    # Usar una expresión regular para encontrar los dobles espacios
    match = re.search(r'\b(\S+)\s{2,}(\S+)', full_name)

    # Dividir el string en palabras individuales
    words = full_name.split()

    if match:
        # Si hay doble espacio, el segundo elemento es el primer nombre
        first_name_index = words.index(match.group(2))  # Obtener la posición detectada
        last_names = words[:first_name_index]  # Todo antes de esa posición son apellidos
        first_names = words[first_name_index:]  # Todo después son nombres
    else:
        # Si no hay doble espacio, los dos primeros son apellidos y el resto son nombres
        last_names = words[:2]  # Primeros dos elementos como apellidos
        first_names = words[2:]  # Resto como nombres

    # Asignar valores
    primer_apellido = last_names[0] if len(last_names) > 0 else ""
    segundo_apellido = last_names[1] if len(last_names) > 1 else ""
    primer_nombre = first_names[0] if len(first_names) > 0 else ""

    # Verificar si el second_surname realmente es el segundo apellido
    return second_surname == segundo_apellido


def find_string_position_contains(array, target_string):
    """
    Busca la posición de la primera ocurrencia de un string que contenga el texto objetivo.

    :param array: Lista de strings donde se realizará la búsqueda.
    :param target_string: Substring que se desea buscar en el array.
    :return: Posición del string en el array (índice) o -1 si no se encuentra.
    """
    for index, value in enumerate(array):
        if target_string in value:
            return index
    return -1  # Devuelve -1 si no se encuentra el substring

def add_spaces_between_characters(s):
    """
    Agrega espacios entre cada carácter de un string, sin agregar espacios al inicio o al final.

    :param s: String de entrada.
    :return: String con espacios entre cada carácter.
    """
    return " ".join(s)

def find_last_matching_string(array, substring):
    """
    Busca en un array el último string que contenga el substring dado.
    
    :param array: Lista de strings donde se realizará la búsqueda.
    :param substring: Subcadena que debe estar contenida en el string buscado.
    :return: Última coincidencia encontrada o None si no hay coincidencias.
    """
    for value in reversed(array):  # Recorrer el array de atrás hacia adelante
        if substring in value:
            return value  # Retornar la última coincidencia encontrada
    return None  # Retornar None si no se encuentra ninguna coincidencia

def extract_rut_data_reordered(pdf_path):
    """
    Extrae nombres completos y números de cédula desde el documento PDF de RUT.
    Se ajusta la lógica para capturar correctamente los valores y validar si hay repeticiones en la misma página.
    """
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        text_lines = text.split("\n")

        id_number = None
        surname1, surname2, first_name, other_names, last_complete_name = "", "", "", "", ""
        found_entries = set()


        for i in range(len(text_lines)):
            line = text_lines[i].strip()
            
            # Buscar la cédula de ciudadanía
            if "Cédula de Ciudadanía" in line:
                for j in range(i + 1, min(i + 5, len(text_lines))):  # Buscar en las siguientes líneas
                    possible_id = text_lines[j].strip().replace(" ", "")
                    if possible_id.isdigit() and len(possible_id) > 6:  # Asegurar que sea un número válido
                        id_number = possible_id
                        break
            
            # Buscar nombres y apellidos en su respectiva sección
            #if page_num == 1:
            #    print(i, "->",line)
            if "Primer apellido" in line and i + 1 < len(text_lines):
                position = find_string_position_contains(text_lines, "@")
                #if page_num == 8 or page_num == 77:
                    #print("text_lines->", text_lines, "\n")
                    #print("position->", position, "\n")
                if text_lines[position-11].strip().replace(" ", "").isdigit():
                    surname1 = text_lines[position-10].strip()
                elif text_lines[position-10].strip().replace(" ", "").isdigit():
                    surname1 = text_lines[position-9].strip()
                else:    
                    surname1 = text_lines[position-11].strip()
                #if page_num == 2:
                #    print("i->",i, "text_lines->", text_lines, "text_lines[i + 1]->", text_lines[i + 1], "surname1->", surname1, '\n')
            if "Segundo apellido" in line and i + 1 < len(text_lines):
                position = find_string_position_contains(text_lines, "@")
                #if page_num == 8 or page_num == 77:
                    #print("text_lines->", text_lines, "\n")
                    #print("position->", position, "\n")
                if text_lines[position-11].strip().replace(" ", "").isdigit():
                    surname2 = text_lines[position-9].strip()
                elif text_lines[position-10].strip().replace(" ", "").isdigit():
                    surname2 = ""
                else:
                    surname2 = text_lines[position-10].strip()
                    
                last_complete_name = find_last_matching_string(text_lines, surname1)
                #if page_num == 2:
                #    print("i->",i, "text_lines->", text_lines, "text_lines[i + 1]->", text_lines[i + 1], "surname2->", surname2, '\n')
            if "Primer nombre" in line and i + 1 < len(text_lines):
                position = find_string_position_contains(text_lines, "@")
                #if page_num == 8 or page_num == 77:
                    #print("text_lines->", text_lines, "\n")
                    #print("position->", position, "\n")
                if text_lines[position-11].strip().replace(" ", "").isdigit():
                    first_name = text_lines[position-8].strip()
                elif text_lines[position-10].strip().replace(" ", "").isdigit():
                    first_name = text_lines[position-8].strip()
                else:
                    first_name = text_lines[position-9].strip()
                #if page_num == 2:
                #    print("i->",i, "text_lines->", text_lines, "text_lines[i + 1]->", text_lines[i + 1], "first_name->", first_name, '\n')
            if "Otros nombres" in line and i + 1 < len(text_lines):
                position = find_string_position_contains(text_lines, "@")
                #if page_num == 8 or page_num == 77:
                    #print("text_lines->", text_lines, "\n")
                    #print("position->", position, "\n")
                if text_lines[position-11].strip().replace(" ", "").isdigit():
                    other_names = ""
                elif text_lines[position-10].strip().replace(" ", "").isdigit():
                    other_names = ""
                else:
                    other_names = text_lines[position-8].strip()
                #if page_num == 2:
                #    print("i->",i, "text_lines->", text_lines, "text_lines[i + 1]->", text_lines[i + 1], "other_names->", other_names, '\n')
        #if page_num == 8 or page_num == 77:
            #print("surname1", surname1, "surname2", surname2, "first_name", first_name, "other_names", other_names, '\n')
                    
        # Construir el nombre completo
        if surname2 == "" and other_names == "":
            full_name = " ".join([first_name, surname1]).strip()
        elif other_names == "" or surname2 == "":
            if len(last_complete_name) < 15:
                full_name = " ".join([first_name, surname1, surname2]).strip()
            else:    
                if reorganize_name(last_complete_name, surname2):
                    full_name = " ".join([first_name, surname1, surname2]).strip()
                else:
                    full_name = " ".join([surname2, first_name, surname1]).strip()
        else:
            full_name = " ".join([first_name, other_names, surname1, surname2]).strip()
        #print("AAAAAAAAAAAAAAid_number->", id_number, "\n")
        if full_name and id_number:
            entry = (full_name, id_number)
            if entry not in found_entries:
                extracted_data.append({
                    "Página": page_num,
                    "Nombre_RUT": full_name,
                    "Cédula_RUT": id_number
                })
                found_entries.add(entry)  # Evitar duplicados en la misma página

    df_rut = pd.DataFrame(extracted_data, columns=["Página", "Nombre_RUT", "Cédula_RUT"])
    return df_rut
