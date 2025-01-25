# src/services/document_service.py
import shutil
import os
import pandas as pd
from src.comparison.comparator import compare_pdf_data
from src.pdf_processing.pdf_vinculation_extractor import extract_vinculation_data
from src.pdf_processing.pdf_declaration_extractor import extract_names_and_ids
from src.pdf_processing.pdf_equivalents_extractor import extract_equivalents_data
from src.pdf_processing.pdf_rut_extractor import extract_rut_data_reordered
from src.pdf_processing.pdf_data_extractor import extract_data_from_pdf

UPLOAD_DIR = "uploaded_files"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def procesar_y_comparar_documentos(files):
    """
    Procesa los archivos PDF, ejecuta la comparación, genera un CSV y retorna estadísticas.

    :param files: Lista de archivos recibidos en la API.
    :return: Diccionario con los datos extraídos, estadísticas y ruta del CSV.
    """
    resultados = {}
    file_paths = {}
    registros_totales = 0

    # Guardar los archivos temporalmente y extraer el número de registros de los nombres
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Obtener número de registros desde el nombre del archivo (los primeros caracteres numéricos)
        num_registros = int("".join(filter(str.isdigit, file.filename.split()[0])))

        registros_totales = max(registros_totales, num_registros)  # El máximo de páginas entre archivos

        # Determinar el tipo de documento según su nombre
        if "Vinculacion" in file.filename:
            file_paths["vinculacion"] = file_path
        elif "Declaracion" in file.filename:
            file_paths["declaracion"] = file_path
        elif "Equivalentes" in file.filename:
            file_paths["equivalentes"] = file_path
        elif "Rut" in file.filename:
            file_paths["rut"] = file_path
        elif "Genesis" in file.filename:
            file_paths["genesis"] = file_path

    # Validar que se hayan identificado exactamente 5 archivos
    if len(file_paths) != 5:
        return {"error": "Se requieren exactamente 5 archivos PDF con los nombres correctos."}

    try:
        # Procesar cada archivo con su función correspondiente
        resultados["vinculacion"] = extract_vinculation_data(file_paths["vinculacion"])
        resultados["declaracion"] = extract_names_and_ids(file_paths["declaracion"])
        resultados["equivalentes"] = extract_equivalents_data(file_paths["equivalentes"])
        resultados["rut"] = extract_rut_data_reordered(file_paths["rut"])
        resultados["genesis"] = extract_data_from_pdf(file_paths["genesis"])

        # Comparar los datos entre los 5 documentos
        df_comparison = compare_pdf_data(file_paths["genesis"], file_paths["declaracion"],
                                         file_paths["equivalentes"], file_paths["rut"],
                                         file_paths["vinculacion"])

        # Guardar los resultados en un CSV
        output_path = os.path.join(OUTPUT_DIR, "comparacion_resultados.csv")
        df_comparison.to_csv(output_path, index=False, encoding="utf-8")
        
         # Convertir DataFrame a lista de diccionarios para enviarlo en la respuesta JSON
        data = df_comparison.to_dict(orient="records")

        # Contar registros con inconsistencias
        registros_con_alteraciones = df_comparison[
            (df_comparison["Coincidencia Nombre"] == False) | (df_comparison["Coincidencia Cédula"] == False)
        ].shape[0]

        registros_con_inconsistencias_nombre = df_comparison[df_comparison["Coincidencia Nombre"] == False].shape[0]
        registros_con_inconsistencias_cedula = df_comparison[df_comparison["Coincidencia Cédula"] == False].shape[0]

        paginas_con_inconsistencias = df_comparison[
            (df_comparison["Coincidencia Nombre"] == False) | (df_comparison["Coincidencia Cédula"] == False)
        ]["Página"].tolist()

        # Eliminar archivos temporales después de la extracción
        for file_path in file_paths.values():
            os.remove(file_path)

        return {
            "message": f"✅ Comparación realizada. Se han guardado {len(df_comparison)} registros en '{output_path}'.",
            "csv_file": output_path,
            "registros_procesados": registros_totales,
            "registros_con_alteraciones": registros_con_alteraciones,
            "registros_con_inconsistencias_nombre": registros_con_inconsistencias_nombre,
            "registros_con_inconsistencias_cedula": registros_con_inconsistencias_cedula,
            "paginas_con_inconsistencias": paginas_con_inconsistencias,
            "data": data  # 🚨 Ahora se envían los datos en JSON
        }

    except Exception as e:
        return {"error": f"Error procesando archivos: {str(e)}"}
